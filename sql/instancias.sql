-- Inserção de dados na tabela ContaCanal
INSERT INTO ContaCanal (Email, Senha, Kids, NumeroVisualizacoes, NumeroInscritos, DataCriacao, Nome)
VALUES
('nathanprediger@gmail.com', 'lalalala', False, 150000, 10000, '2018-03-15', 'Canal Culinária Divina'),
('gabrielricci@gmail.com', 'lolololo', False, 500000, 40000, '2020-07-20', 'Mundo Tech'),
('andrefrainer@gmail.com', 'opaopaopa', True, 30000, 2500, '2021-12-05', 'Diversão para Crianças'),
('rodrigobagrilli@gmail.com', 'bahtche', False, 120000, 8000, '2017-05-10', 'Viagem e Aventuras'),
('isavidor@gmail.com', 'salsichao', False, 200000, 15000, '2019-11-25', 'Mundo Fitness'),
('marianabanana@gmail.com', 'alanturing', False, 250000, 20000, '2020-09-10', 'Ciência todo dia'),
('giselerotta@gmail.com', '123456', False, 180000, 12000, '2019-08-05', 'Mundo das Artes'),
('alinefraga@gmail.com', 'fallengoat', False, 350000, 45000, '2021-01-20', 'Pro Gaming');

-- Inserção de dados na tabela Post
INSERT INTO Post (IDCanal, Likes, Dislikes, DataPublicacao)
VALUES
(1, 800, 15, '2023-03-01'),
( 2, 1500, 50, '2023-01-20'),
( 3, 300, 5, '2023-02-10'),
( 4, 1200, 10, '2023-02-25'),
( 5, 600, 20, '2023-03-05'),
( 6, 2000, 30, '2023-03-10'),
( 7, 1700, 25, '2023-03-15'),
( 8, 5000, 50, '2023-03-20'),
( 1, 0, 5000, '2023-03-20'),
( 2, 1200, 30, '2012-04-01'), 
( 3, 2500, 40, '2008-04-10'), 
( 4, 900, 25, '2015-04-15'); 
-- Inserção de dados na tabela PostComunidade
INSERT INTO PostComunidade (IDPost, Texto, Imagem)
VALUES
(1, 'Pessoal novo vídeo no canal hoje sobre uma torta deliciosa, fiquem ligados hein! ', NULL),
(2, 'O que acharam do novo S24? Logo logo sai a análise no canal', NULL),
(3, 'Olá pequenos e pequenas! Hoje tem uma aventura nova saindo no canal! Preparados?', NULL),
(4, 'Quem aí já viajou pra Alemanha? Vou lançar umas dicas no canal em breve', NULL),
(5, 'Dicas para começar sua jornada no mundo fitness.', NULL),
(6, 'Descubra os segredos do universo no meu último vídeo! ', NULL),
(7, 'Arte abstrata: o que é e como explorar sua criatividade!', NULL),
(8, 'Dicas para nunca mais perder uma partida no Counter-Strike! ', NULL),
(12, REPEAT('A',501),NULL),
(9, 'Pessoal o que acharam do último vídeo? Gostaram do formato?', NULL),
(10, 'Olhem esse meme de IA que eu encontrei no facebook kkkkkkkkk', NULL),
(11, 'Deixem suas sugestões de vídeos nos comentários!', NULL);

-- Inserção de dados na tabela Video
INSERT INTO Video (IDPost, Short, Descricao, Resolucao, Duracao, NumeroVisualizacoes, Titulo)
VALUES
(1, False, 'Aprenda a fazer uma torta de limão deliciosa.', '1080p', 600, 80000, 'Torta de Limão Incrível'),
(2, False, 'Review completo no novo S24.', '4K', 900, 120000, 'Novo S24'),
(3, True, 'Pequena história em animação para crianças.', '720p', 180, 5000, 'Aventura Espacial'),
(4, False, 'Dicas de viagem para a Alemanha.', '1080p', 1200, 75000, 'Alemanha: dúvidas'),
(5, False, 'Treino prático para iniciantes.', '1080p', 300, 45000, 'Treino Fitness'),
(6, False, 'Experimento incrível sobre leis de Newton.', '1080p', 720, 100000, 'Leis de Newton'),
(7, False, 'Técnicas para criar pinturas abstratas.', '720p', 600, 75000, 'Arte Abstrata'),
(8, True, 'Jogada épica no Major de Counter-Strike.', '4K', 180, 150000, 'Jogada insana do Coldzera'),
(9, False, 'Como temperar carnes como um chefe.', '1080p', 500, 70000, 'Temperando Carnes'),
(10, False, 'Análise detalhada do impacto da IA no dia a dia.', '4K', 1200, 90000, 'Impacto da IA'),
(11, False, 'Treino funcional para iniciantes.', '1080p', 300, 50000, 'Treino Funcional');


-- Inserção de dados na tabela Playlist
INSERT INTO Playlist (ID, IDCanal, DataCriacao, Nome)
VALUES
(1, 1, '2022-12-01', 'Sobremesas Deliciosas'),
(2, 2, '2023-01-15', 'Tecnologia Inovadora'),
(3, 4, '2022-05-10', 'Viagem pelo Mundo'),
(4, 6, '2023-02-01', 'Experimentos Científicos'),
(5, 7, '2023-03-01', 'Arte e Criatividade'),
(6, 8, '2023-03-10', 'Jogadas Absurdas');

-- Inserção de dados na tabela PlaylistVideo
INSERT INTO PlaylistVideo (IDPlaylist, IDVideo)
VALUES
(1, 1),
(2, 2),
(3, 4),
(4, 6),
(5, 7),
(6, 8),
(1, 9),
(2, 10), 
(3, 11); 

-- Inserção de dados na tabela Anuncio
INSERT INTO Anuncio (CNPJ, Conteudo, Link, Duracao)
VALUES
('12345678000199', 'Promoção imperdível: utensílios de cozinha.', 'http://tramontina.com/utensilios', 30),
('98765432000188', 'Tecnologia que transforma seu dia.', 'http://samsung.com', 45),
('11223344000155', 'Viaje com descontos especiais.', 'http://trivago.com/promocoes', 60),
('33445566000122', 'Promoção: livros de ciência para todas as idades.', 'http://mundociencia.com/livros', 60),
('55667788000144', 'Kits de pintura e arte para iniciantes.', 'http://faber-castell.com/kits', 45),
('77889900000133', 'Descontos em periféricos gamers.', 'http://terabyte.com/perifericos', 30),
('99988877000166', 'Utensílios premium para chefs.', 'http://tramontina.com/utensilios', 45),
('66655544000122', 'Cursos de inteligência artificial.', 'http://alura.com/ia', 60);

-- Inserção de dados na tabela AnuncioCanal
INSERT INTO AnuncioCanal (IDAnuncio, IDCanal, Exibicoes, Cliques)
VALUES
(1, 1, 10000, 200),
(2, 2, 20000, 800),
(3, 4, 5000, 100),
(4, 6, 15000, 300),
(5, 7, 10000, 250),
(6, 8, 40000, 1000),
(7, 1, 20000, 400), 
(8, 2, 25000, 500); 

-- Inserção de dados na tabela Comentario
INSERT INTO Comentario (ID, IDPost, IDPostAlvo, Texto)
VALUES
(1, 1, 1, 'Adorei a receita, vou fazer!'),
(2, 2, 2, 'Ótima análise do novo celular da Samsung, parabéns!'),
(3, 4, 4, 'Já estou planejando minha viagem para a alemanha depois dessas dicas.'),
(4, 6, 6, 'Experimento irado! Posso fazer em casa?'),
(5, 7, 7, 'Que técnicas incríveis, vou tentar usar elas!'),
(6, 8, 8, 'Depois dessa jogada ficou claro que Coldzera >>>> Simple'),
(7, 9, 9, 'Essas dicas transformaram meus pratos! O pessoal aqui de casa está pedindo o segredo! kkkkk'),
(8, 10, 10, 'Será que as IA irão dominar o planeta??? Estou com medo!!!'),
(9, 11, 11, 'Treino rápido e eficaz, assim consigo encaixar na minha escala 6x1 #FIMESCALA6X1');
