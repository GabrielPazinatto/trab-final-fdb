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
        print("3 - Playlists com mais de [x] vídeos e canal criador.")
        print("4 - Canais que nao postaram nenhum vídeo com resolução menor que 720p e menos de [x] visualizações.")
        print("5 - [x] Canais com melhor taxa de cliques/tempo de exibição no anúncio com id [y]")
        print("6 - Canais com posts de comunidade maior que [x] caracteres.")

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
                print(QUERIES.get_videos_from_playlists_whith_x_subscribers(DB_CONNECTION, DB_CURSOR, n))
            case 3:
                print("Quantidade de vídeos mínima: ")
                try:
                    n = int(input())
                except ValueError:
                    print("Valor inválido.")
                    break
                #print(QUERIES.get_)
          
            case 4:
                print("Quantidade de visualizações: ")
                try:
                    n = int(input())
                except ValueError:
                    print("Valor inválido.")
                    break
                print(QUERIES.get_channels_with_no_low_res_low_view_videos(DB_CONNECTION, DB_CURSOR, n))
                
            case 5:
                try:
                    print("Quantidade de canais: ")
                    quantity = int(input())
                except ValueError:
                    quantity = -1
                    print("ID do anúncio: ")
                ad_id = int(input())
                print(QUERIES.get_top_channels_by_click_rate(DB_CONNECTION, DB_CURSOR, ad_id, quantity))

            case 6:
                print("Tamanho mínimo do post de comunidade: ")
                try:
                    n = int(input())
                except ValueError:
                    print("Valor inválido.")
                    break
                print(QUERIES.get_channels_community_posts(DB_CONNECTION, DB_CURSOR, n))

                

        #print("3 - Número de vídeos e comentários por canal.")
        #print("4 - ")



