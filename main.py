from Database import Database
from Queries import Queries
from Views import Views

DATABASE_PORT = 5432
DATABASE_HOST = "localhost"
DATABASE_NAME = "youtube"
DATABASE_USER = "postgres"
DATABASE_PASSWORD = "root"

DATABASE = Database(port=DATABASE_PORT, host=DATABASE_HOST, dbname=DATABASE_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD)
DB_CONNECTION = DATABASE.get_connection()
DB_CURSOR = DATABASE.get_cursor()

QUERIES = Queries()
VIEWS = Views()


if __name__ == "__main__":
    
    view_created:bool = False
    opt:int = 0
    while(opt != -1):
        print("\n1 - Criar view DetalhesVideos.")
        print("2 - Videos em playlists Cujos canais possuem mais de [x] inscritos.")
        print("3 - Canais com playlists com mais de [x] videos.")
        print("4 - Canais que nao postaram nenhum vídeo com resolução menor que 720p e menos de [x] visualizações.")
        print("5 - [x] Canais com melhor taxa de cliques/tempo de exibição no anúncio com id [y]")
        print("6 - Inscritos do canal com id [x]")
        print("7 - Feed do canal com id [x]")
        print("8 - Inserir Video")
        if view_created:
            print("9 - Canais com posts de comunidade maior que [x] caracteres.")
            print("10 - Canais com mais vídeos publicado que a média por canal")
            print("11 - Vídeos que possuem mais comentários que a média por vídeo")
            print("12 - Número de videos e comentários por canal")

        opt = int(input("\nDigite a opção desejada: "))

        match(opt):
            case 1:
                try:
                    VIEWS.create_view_detalhes_videos(DB_CONNECTION, DB_CURSOR)
                    view_created = True
                    print("View criada com sucesso.")
                except Exception as e:
                    print("Erro ao criar view: ", e)
            case 2:
                print("Quantidade de inscritos mínima: ")
                try:
                    n = int(input())
                except ValueError:
                    print("Valor inválido.")
                    break
                for t in QUERIES.get_videos_from_playlists_whith_x_subscribers(DB_CONNECTION, DB_CURSOR, n):
                    print(t)
            case 3:
                print("Quantidade de vídeos mínima: ")
                try:
                    n = int(input())
                except ValueError:
                    print("Valor inválido.")
                    break
                for t in QUERIES.get_channels_with_playlists_over_x_videos(DB_CONNECTION, DB_CURSOR, n):
                    print(t)

            case 4:
                print("Quantidade de visualizações: ")
                try:
                    n = int(input())
                except ValueError:
                    print("Valor inválido.")
                    break
                for t in QUERIES.get_channels_with_no_low_res_low_view_videos(DB_CONNECTION, DB_CURSOR, n):
                    print(t) 
                
            case 5:
                try:
                    print("Quantidade de canais: ")
                    quantity = int(input())
                except ValueError:
                    quantity = -1

                print("ID do anúncio: ")
                ad_id = int(input())
                for t in (QUERIES.get_top_channels_by_click_rate(DB_CONNECTION, DB_CURSOR, ad_id, quantity)):
                    print(t)
            
            case 6:
                try:
                    print("ID do canal: ")
                    channel = int(input())
                except ValueError:
                    channel = -1
                
                for t in (QUERIES.get_subscriptions(DB_CONNECTION, DB_CURSOR, channel)):
                    print(t)
                    
            case 7:
                try:
                    print("ID do canal: ")
                    channel = int(input())
                except ValueError:
                    channel = -1
                
                for t in (QUERIES.get_feed(DB_CONNECTION, DB_CURSOR, channel)):
                    print(t)

            case 8:
                
                print("""(IDPost=IDPost,
                    IDCanal,
                    Likes,
                    Dislikes,
                    DataPublicacao,
                    Short,
                    Descricao,
                    Resolucao,
                    Duracao,
                    NumeroVisualizacoes,
                    Titulo)""")
                attributes = input().split(",")

                print(attributes)

                IDCanal = int(attributes[0].strip())
                Likes = int(attributes[1].strip())
                Dislikes = int(attributes[2].strip())
                DataPublicacao = attributes[3].strip()  
                Short = attributes[4].strip().lower() == "true" 
                Descricao = attributes[5].strip()
                Resolucao = attributes[6].strip()
                Duracao = int(attributes[7].strip())
                NumeroVisualizacoes = int(attributes[8].strip())
                Titulo = attributes[9].strip()
                quantity = int(attributes[10].strip()) if len(attributes) > 12 else -1  
                
                
                QUERIES.insert_video(cursor=DB_CURSOR,
                    connection=DB_CONNECTION,
                    IDCanal=IDCanal,
                    Likes=Likes,
                    Dislikes=Dislikes,
                    DataPublicacao=DataPublicacao,
                    Short=Short,
                    Descricao=Descricao,
                    Resolucao=Resolucao,
                    Duracao=Duracao,
                    NumeroVisualizacoes=NumeroVisualizacoes,
                    Titulo=Titulo,
                )
                    
            
            case 9:
                print("Tamanho mínimo do post de comunidade: ")
                try:
                    n = int(input())
                except ValueError:
                    print("Valor inválido.")
                    break
                for t in (QUERIES.get_channels_community_posts(DB_CONNECTION, DB_CURSOR, n)):
                    print(t)

            case 10:
                for t in (QUERIES.get_channels_with_above_average_videos(DB_CONNECTION, DB_CURSOR)):
                    print(t)

            case 11: 
                for t in (QUERIES.get_videos_with_above_average_comments(DB_CONNECTION, DB_CURSOR)):
                    print(t)

            case 12: 
                for t in (QUERIES.get_channels_with_total_videos_and_comments(DB_CONNECTION,DB_CURSOR)):
                    print(t)
                

        #print("3 - Número de vídeos e comentários por canal.")
        #print("4 - ")



