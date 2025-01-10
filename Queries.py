import psycopg

class Queries:

    def __init__(self) -> None:
        pass


    # Listar os canais com o número total de vídeos e a quantidade total de comentários que receberam em seus vídeos, agrupados por canal.
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
    # Listar os canais que possuem playlists com mais de 5 vídeos, mostrando o nome do canal, o número total de playlists e o total de vídeos nessas playlists.
    def get_channels_with_playlists_over_5_videos(
        self, connection: psycopg.Connection, cursor: psycopg.Cursor, vid_quantity:int = 0, quantity: int = -1
    ):
        cursor.execute(
            """
            SELECT 
                ContaCanal.ID AS IDCanal,
                ContaCanal.Nome AS NomeCanal,
                COUNT(DISTINCT Playlist.ID) AS TotalPlaylists,
                COUNT(PlaylistVideo.IDVideo) AS TotalVideos
            FROM 
                ContaCanal
            JOIN 
                Playlist ON ContaCanal.ID = Playlist.IDCanal
            JOIN 
                PlaylistVideo ON Playlist.ID = PlaylistVideo.IDPlaylist
            GROUP BY 
                ContaCanal.ID, ContaCanal.Nome
            HAVING 
                COUNT(PlaylistVideo.IDVideo) > %s
            ORDER BY 
                TotalVideos DESC;
            """,
            (vid_quantity,)
        )

        connection.commit()

        if quantity == -1:
            return cursor.fetchall()
        else:
            return cursor.fetchmany(quantity)

    # Identifica vídeos que possuem mais (maior ou igual) comentários do que a média de comentários por vídeo no sistema.
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

    # Identifica canais que publicaram mais vídeos do que a média de vídeos por canal.
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

    # Retorna os ID de todos dos vídeos que estão em playlists e que pertencem a canais com mais de [x] inscritos.
    def get_videos_from_playlists_whith_x_subscribers(
        self, connection: psycopg.Connection, cursor: psycopg.Cursor, quantity: int = -1
    ):
        cursor.execute(
            """
            SELECT DISTINCT PlaylistVideo.IDVideo
            FROM PlaylistVideo
            WHERE PlaylistVideo.IDVideo NOT IN (
                SELECT Video.ID
                FROM Video
                JOIN Post ON Video.IDPost = Post.ID
                JOIN ContaCanal ON Post.IDCanal = ContaCanal.ID
                WHERE ContaCanal.NumeroInscritos <= 1000
            );
            """
        )

        connection.commit()

        if quantity == -1:
            return cursor.fetchall()
        else:
            return cursor.fetchmany(quantity)

    # Retorna o ID e o Nome dos canais que não publicaram nenhum vídeo com resolução inferior a 720p e menos de 100 visualizações.
    def get_channels_with_no_low_res_low_view_videos(
        self, connection: psycopg.Connection, cursor: psycopg.Cursor, quantity: int = -1
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
                AND Video.NumeroVisualizacoes < 100
            );
            """
        )

        connection.commit()

        if quantity == -1:
            return cursor.fetchall()
        else:
            return cursor.fetchmany(quantity)

    # Retorna os [x] canais com melhor taxa de cliques/tempo de exibição do canal (soma da duração de todos os seus vídeos) de um anúncio [y].
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


    # Identifica canais que publicaram posts de comunidade com textos longos (mais de 500 caracteres).
    def get_channels_community_posts(
        self, connection: psycopg.Connection, cursor: psycopg.Cursor, post_size:int = -1, quantity: int = -1
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
                CHAR_LENGTH(PostComunidade.Texto) > 500
            GROUP BY 
                ContaCanal.ID, ContaCanal.Nome
            ORDER BY 
                TotalPostsLongos DESC;
            """
        )

        connection.commit()

        if quantity == -1:
            return cursor.fetchall()
        else:
            return cursor.fetchmany(quantity)
