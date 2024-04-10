from PIL import Image
import unidecode

def image_fundo(nome, telefone):
    # Abrir as duas imagens
    imagem_superior = Image.open("photo_selfie.jpg")
    imagem_inferior = Image.open("new_fundo.png")

    # Verificar qual imagem é maior em largura
    largura_total = max(imagem_superior.width, imagem_inferior.width)

    # Criar uma nova imagem com a largura total e a altura somada das duas imagens
    altura_total = imagem_superior.height + imagem_inferior.height
    imagem_combinada = Image.new("RGB", (largura_total, altura_total))

    # Colar a imagem superior no topo
    imagem_combinada.paste(imagem_superior, (0, 0))

    # Colar a imagem inferior no rodapé
    imagem_combinada.paste(imagem_inferior, (0, imagem_superior.height))

    # Salvar a imagem combinada
    string = "photos/photo_"+unidecode.unidecode(nome)+"_"+telefone+".jpg"
    imagem_combinada.save(string)
