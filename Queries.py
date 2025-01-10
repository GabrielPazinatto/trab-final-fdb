import psycopg

class Queries:
    def __init__(self) -> None:
        pass

    # (9) Listar os canais com o número total de vídeos e a quantidade total de comentários que receberam em seus vídeos, agrupados por canal.
    def get_channels_with_total_videos_and_comments(
        self, connection: psycopg.Connection, cursor: psycopg.Cursor, quantity: int = -1
    ):
        cursor.execute(
            """
            SELECT 
                DetalhesVideos.IDCanal,
                DetalhesVideos.NomeCanal,
                COUNT(Video.ID) AS TotalVideos,
                COUNT(Comentario.ID) AS TotalComentarios
            FROM 
                DetalhesVideos
            LEFT JOIN 
                Video ON DetalhesVideos.IDVideo = Video.ID
            LEFT JOIN 
                Comentario ON Video.ID = Comentario.IDPostAlvo
            GROUP BY 
                DetalhesVideos.IDCanal, DetalhesVideos.NomeCanal
            ORDER BY 
                TotalVideos DESC;
            """
        )

        connection.commit()

        if quantity == -1:
            return cursor.fetchall()
        else:
            return cursor.fetchmany(quantity)

    # (3) Listar os canais que possuem playlists com mais de [x] vídeos, mostrando o nome do canal, o número total de playlists e o total de vídeos nessas playlists.
    def get_channels_with_playlists_over_x_videos(
        self,
        connection: psycopg.Connection,
        cursor: psycopg.Cursor,
        vid_quantity: int = 0,
        quantity: int = -1,
    ):
        cursor.execute(
            """
            SELECT 
                ContaCanal.ID AS IDCanal,
                ContaCanal.Nome AS NomeCanal,
                Playlist.Nome,
                COUNT(DISTINCT Playlist.ID) AS TotalPlaylists,
                COUNT(PlaylistVideo.IDVideo) AS TotalVideos
            FROM 
                ContaCanal
            JOIN 
                Playlist ON ContaCanal.ID = Playlist.IDCanal
            JOIN 
                PlaylistVideo ON Playlist.ID = PlaylistVideo.IDPlaylist
            GROUP BY 
                ContaCanal.ID, ContaCanal.Nome, Playlist.Nome
            HAVING 
                COUNT(PlaylistVideo.IDVideo) > %s
            ORDER BY 
                TotalVideos DESC;
            """,
            (vid_quantity,),
        )

        connection.commit()

        if quantity == -1:
            return cursor.fetchall()
        else:
            return cursor.fetchmany(quantity)

    # (8) Identifica vídeos que possuem mais (maior ou igual) comentários do que a média de comentários por vídeo no sistema.
    def get_videos_with_above_average_comments(
        self, connection: psycopg.Connection, cursor: psycopg.Cursor, quantity: int = -1
    ):
        cursor.execute(
            """
            SELECT 
                DetalhesVideos.IDVideo,
                DetalhesVideos.TituloVideo,
                DetalhesVideos.NomeCanal,
                (SELECT COUNT(Comentario.ID) 
                 FROM Comentario 
                 WHERE Comentario.IDPostAlvo = DetalhesVideos.IDVideo) AS TotalComentarios
            FROM 
                DetalhesVideos
            WHERE 
                (SELECT COUNT(Comentario.ID) 
                 FROM Comentario 
                 WHERE Comentario.IDPostAlvo = DetalhesVideos.IDVideo) >=
                (SELECT AVG(ComentarioCount.Total) 
                 FROM (
                     SELECT COUNT(Comentario.ID) AS Total
                     FROM Comentario
                     GROUP BY Comentario.IDPostAlvo
                 ) AS ComentarioCount);
            """
        )

        connection.commit()

        if quantity == -1:
            return cursor.fetchall()
        else:
            return cursor.fetchmany(quantity)

    # (7) Identifica canais que publicaram mais vídeos do que a média de vídeos por canal.
    def get_channels_with_above_average_videos(
        self, connection: psycopg.Connection, cursor: psycopg.Cursor, quantity: int = -1
    ):
        cursor.execute(
            """
            SELECT 
                DetalhesVideos.IDCanal,
                DetalhesVideos.NomeCanal,
                COUNT(DetalhesVideos.IDVideo) AS TotalVideos
            FROM 
                DetalhesVideos
            GROUP BY 
                DetalhesVideos.IDCanal, DetalhesVideos.NomeCanal
            HAVING 
                COUNT(DetalhesVideos.IDVideo) >
                (SELECT AVG(VideoCount.Total)
                 FROM (
                     SELECT COUNT(Video.ID) AS Total
                     FROM Video
                     JOIN Post ON Video.IDPost = Post.ID
                     GROUP BY Post.IDCanal
                 ) AS VideoCount);
            """
        )

        connection.commit()

        if quantity == -1:
            return cursor.fetchall()
        else:
            return cursor.fetchmany(quantity)

    # (2) Retorna os vídeos que estão em playlists e que pertencem a canais com mais de [x] inscritos.
    def get_videos_from_playlists_whith_x_subscribers(
        self,
        connection: psycopg.Connection,
        cursor: psycopg.Cursor,
        quant_subs: int,
        quantity: int = -1,
    ):
        cursor.execute(
            """
            SELECT DISTINCT Video.ID, Video.Titulo, Video.Resolucao, Video.NumeroVisualizacoes, Video.Duracao
            FROM PlaylistVideo
            JOIN Video ON PlaylistVideo.IDVideo = Video.ID
            WHERE PlaylistVideo.IDVideo NOT IN (
                SELECT Video.ID
                FROM Video
                JOIN Post ON Video.IDPost = Post.ID
                JOIN ContaCanal ON Post.IDCanal = ContaCanal.ID
                WHERE ContaCanal.NumeroInscritos <= %s
            );
            """,
            (quant_subs,),
        )

        connection.commit()

        if quantity == -1:
            return cursor.fetchall()
        else:
            return cursor.fetchmany(quantity)

    # (4) Retorna o ID e o Nome dos canais que não publicaram nenhum vídeo com resolução inferior a 720p e menos de [x] visualizações.
    def get_channels_with_no_low_res_low_view_videos(
        self,
        connection: psycopg.Connection,
        cursor: psycopg.Cursor,
        n_views: int = 0,
        quantity: int = -1,
    ):
        cursor.execute(
            """
            SELECT ContaCanal.ID, ContaCanal.Nome
            FROM ContaCanal
            WHERE NOT EXISTS (
                SELECT *
                FROM Video
                JOIN Post ON Video.IDPost = Post.ID
                WHERE Post.IDCanal = ContaCanal.ID
                AND Video.Resolucao < '720p'
                AND Video.NumeroVisualizacoes < %s
            );
            """,
            (n_views,),
        )

        connection.commit()

        if quantity == -1:
            return cursor.fetchall()
        else:
            return cursor.fetchmany(quantity)

    # (5) Retorna os [x] canais com melhor taxa de cliques/tempo de exibição do canal (soma da duração de todos os seus vídeos) de um anúncio [y].
    def get_top_channels_by_click_rate(
        self,
        connection: psycopg.Connection,
        cursor: psycopg.Cursor,
        ad_id: int,
        quantity: int = -1,
    ):
        cursor.execute(
            """
            SELECT 
                ContaCanal.ID AS IDCanal,
                ContaCanal.Nome AS NomeCanal,
                SUM(Video.Duracao) AS TempoTotalVideos,
                CAST(SUM(AnuncioCanal.Cliques) AS FLOAT) / SUM(Video.Duracao) AS TaxaCliquesPorTempo 
            FROM 
                ContaCanal
            JOIN 
                AnuncioCanal ON ContaCanal.ID = AnuncioCanal.IDCanal
            JOIN 
                Anuncio ON AnuncioCanal.IDAnuncio = Anuncio.ID
            JOIN 
                Post ON ContaCanal.ID = Post.IDCanal
            JOIN 
                Video ON Post.ID = Video.IDPost
            WHERE 
                Anuncio.ID = %s
            GROUP BY 
                ContaCanal.ID, ContaCanal.Nome
            HAVING 
                SUM(Video.Duracao) > 0
            ORDER BY 
                TaxaCliquesPorTempo DESC
            """,
            (ad_id,),
        )

        connection.commit()

        if quantity == -1:
            return cursor.fetchall()
        else:
            return cursor.fetchmany(quantity)

    # (6) Identifica canais que publicaram posts de comunidade com textos mais longos que [x] caracteres.
    def get_channels_community_posts(
        self,
        connection: psycopg.Connection,
        cursor: psycopg.Cursor,
        post_length: int = 500,
        quantity: int = -1,
    ):
        cursor.execute(
            """
            SELECT 
                ContaCanal.ID AS IDCanal,
                ContaCanal.Nome AS NomeCanal,
                COUNT(PostComunidade.ID) AS TotalPostsLongos,
                AVG(Post.Likes) AS MediaLikes
            FROM 
                ContaCanal
            JOIN 
                Post ON ContaCanal.ID = Post.IDCanal
            JOIN 
                PostComunidade ON Post.ID = PostComunidade.IDPost
            WHERE 
                CHAR_LENGTH(PostComunidade.Texto) > %s
            GROUP BY 
                ContaCanal.ID, ContaCanal.Nome
            ORDER BY 
                TotalPostsLongos DESC;
            """,
            (post_length,),
        )

        connection.commit()

        if quantity == -1:
            return cursor.fetchall()
        else:
            return cursor.fetchmany(quantity)

    def get_subscriptions(
        self,
        connection: psycopg.Connection,
        cursor: psycopg.Cursor,
        channel: int = 0,
        quantity: int = -1,
    ):
        cursor.execute(
            """
            SELECT
                C2.ID, C2.Nome, I.IDFonte
            FROM
                Inscricoes I 
            JOIN 
                ContaCanal C1 ON (I.IDDestino = C1.ID) 
            JOIN
                ContaCanal C2 ON (I.IDFonte = C2.ID)
            WHERE
                I.IDDestino = %s
            """,
            (channel,),
        )

        connection.commit()

        if quantity == -1:
            return cursor.fetchall()
        else:
            return cursor.fetchmany(quantity)

    def get_feed(
        self,
        connection: psycopg.Connection,
        cursor: psycopg.Cursor,
        channel: int = 0,
        quantity: int = -1,
    ):
        cursor.execute(
            """
            SELECT
                Feed.IDCanal, Feed.IDVideo, Video.Titulo
            FROM
                Feed 
            JOIN
                Video ON (Feed.IDVideo = Video.ID)
            WHERE
                Feed.IDCanal = %s
            """,
            (channel,),
        )

        connection.commit()

        if quantity == -1:
            return cursor.fetchall()
        else:
            return cursor.fetchmany(quantity)

    def insert_video(
        self,
        connection: psycopg.Connection,
        cursor: psycopg.Cursor,
        IDCanal: int = 0,
        Likes: int = 0,
        Dislikes: int = 0,
        DataPublicacao: str = "",
        Short: bool = False,
        Descricao: str = "",
        Resolucao: str = "",
        Duracao: int = 0,
        NumeroVisualizacoes: int = 0,
        Titulo: str = "",
    ):
        cursor.execute(
            """
            INSERT INTO Post (IDCanal, Likes, Dislikes, DataPublicacao)
            VALUES (%s, %s, %s, %s)
            RETURNING ID;
            """,
            (IDCanal, Likes, Dislikes, DataPublicacao)
        )
        result = cursor.fetchone()
        if result is None:
            raise ValueError("Failed to insert post and retrieve ID.")
        post_id = result[0]

        cursor.execute(
            """
            INSERT INTO Video (IDPost, Short, Descricao, Resolucao, Duracao, NumeroVisualizacoes, Titulo)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            """,
            (post_id, Short, Descricao, Resolucao, Duracao, NumeroVisualizacoes, Titulo)
        )

        connection.commit()


# CREATE TABLE Post(
# 	ID SERIAL NOT NULL,
# 	IDCanal INT NOT NULL,
# 	Likes INT NOT NULL,
# 	Dislikes INT NOT NULL,
# 	DataPublicacao DATE NOT NULL,
# 	PRIMARY KEY(ID),
# 	FOREIGN KEY(IDCanal) REFERENCES ContaCanal(ID) ON DELETE CASCADE
# );

# CREATE TABLE Video(
# 	ID SERIAL NOT NULL,
# 	IDPost INT NOT NULL,
# 	Short BOOLEAN NOT NULL,
# 	Descricao VARCHAR(1000) NOT NULL,
# 	Resolucao CHAR(9) NOT NULL,
# 	Duracao INT NOT NULL,
# 	NumeroVisualizacoes INT NOT NULL,
# 	Titulo VARCHAR(30) NOT NULL,
# 	PRIMARY KEY(ID),
# 	FOREIGN KEY(IDPost) REFERENCES Post(ID) ON DELETE CASCADE
# );
