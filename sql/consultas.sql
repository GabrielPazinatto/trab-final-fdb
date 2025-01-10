-- Essa visão reúne informações sobre vídeos publicados, suas descrições, número de visualizações e a qual canal pertencem. 
-- Isso pode ser útil para gerenciar os vídeos e avaliar o desempenho por canal, bem como suas métricas em geral.
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

--Listar os canais com o número total de vídeos e a quantidade total de comentários que receberam em seus vídeos, agrupados por canal.
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

-- Listar os canais que possuem playlists com mais de 5 vídeos, mostrando o nome do canal, o número total de playlists e o total de vídeos nessas playlists.

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
    COUNT(PlaylistVideo.IDVideo) > 5
ORDER BY 
    TotalVideos DESC;

-- Essa consulta identifica vídeos que possuem mais (maior ou igual) comentários do que a média de comentários por vídeo no sistema, retornando o ID, o título, o nome do canal a qual pertence e a quantidade de comentários do Vídeo
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
     ) AS ComentarioCount) ;


-- Essa consulta identifica canais que publicaram mais vídeos do que a média de vídeos por canal, retornando o ID, o nome e o total de vídeos do canal

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

-- Essa consulta retorna os ID de todos dos vídeos que estão em playlists e que pertencem a canais com mais de 1.000 inscritos.

SELECT DISTINCT PlaylistVideo.IDVideo
FROM PlaylistVideo
WHERE PlaylistVideo.IDVideo NOT IN (
    SELECT Video.ID
    FROM Video
    JOIN Post ON Video.IDPost = Post.ID
    JOIN ContaCanal ON Post.IDCanal = ContaCanal.ID
    WHERE ContaCanal.NumeroInscritos <= 1000
);

-- Essa consulta retorna o ID e o Nome dos canais que não publicaram nenhum vídeo com resolução inferior a 720p e menos de [x] visualizações.
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

-- Essa consula, dado o ID de um anúncio, retorna os 5 canais com melhor taxa de cliques/tempo de exibição do canal (soma da duração de todos os seus vídeos) desse anúncio 

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
    Anuncio.ID = 3 -- Selecionar o ID de um anúncio {Ex: Anuncio.ID = 3}
GROUP BY 
    ContaCanal.ID, ContaCanal.Nome
HAVING 
    SUM(Video.Duracao) > 0
ORDER BY 
    TaxaCliquesPorTempo DESC
LIMIT 5;

--Essa consulta identifica canais que publicaram posts de comunidade com textos longos (mais de 500 caracteres) e retorna o nome do canal, o número total de posts de comunidade longos, e a média de likes nos posts desses canais.
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

