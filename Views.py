import psycopg

class Views:
    def create_view_detalhes_videos(self, connection: psycopg.Connection, cursor: psycopg.Cursor):
        cursor.execute(
            """
            CREATE VIEW DetalhesVideos AS
            SELECT 
                Video.ID AS IDVideo,
                Video.Titulo AS TituloVideo,
                Video.Descricao AS Descricao,
                Video.NumeroVisualizacoes AS Visualizacoes,
                Video.Duracao AS Duracao,
                ContaCanal.ID AS IDCanal,
                ContaCanal.Nome AS NomeCanal,
                ContaCanal.NumeroInscritos AS InscritosCanal
            FROM 
                Video
            JOIN 
                Post ON Video.IDPost = Post.ID
            JOIN 
                ContaCanal ON Post.IDCanal = ContaCanal.ID;
            """
        )
        connection.commit()
