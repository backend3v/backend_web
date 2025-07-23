import subprocess,json,re
from deep_translator import GoogleTranslator

class BitoService:
    def __init__(self,outputLang='en'):
        self.outputLang = outputLang
        self.languajes= {
            "es":"Spanish",
            "en":"English",
            "fr":"French",
            "de":"German",
            "it":"Italian",
            "pt":"Portuguese",
            "ru":"Russian",
            "zh":"Chinese",
            "ja":"Japanese",
            "ko":"Korean"
        }
    def getConfigList(self):
        result = subprocess.run([ 'bito','config','-e'], capture_output=True, text=True, check=True)
        return result
    def getPrompt(self,prompt_text):
        return f"""
        noticias:Traeme las 3 noticias mas importantes actualmente sobre {prompt_text} tienen que ser noticias relevantes y no mas antiguas de 1 semana de preferencia noticias que hayan sido polemicas, importantes y relevantes para {prompt_text}, deben ser descriptivas y con un estilo periodistico, deben tener los detalles y no dejar temas inconclusos, deben ser cortas pero completas, traer nombres propios, lugares, y muy importante deben tener la fecha de su publicacion y la fuente en la descripcion de esta noticia, buscalas de fuentes oficiales y evita en lo posible fake news y fuentes de dudosa procedencia
        comparativa:hazme un csv con campos que se puedan usar para generar un grafico comparativo, busca valores comparables puede ser entre tiempo,region,items afines o contrarios, algun contexto sobre las noticias generadas o otros factores que puedan ser relevantes; sobre el tema de {prompt_text}, estos valores deben ser solamente numericos y en lo posible cercanos, teniendo en cuneta que esta comparativa sera preparada para un grafico tipo linea en donde es importante que los valores no sean demasiado lejanos y que sean representativos de lo que se quiere comparar, la comparativa debe tener minimo 4 columnas en lo posible y que tengan relacion entre si si es posible
        imagen:Traeme una imagen acerca de {prompt_text}, si se trata de una organizacion, empresa, institucion o algo que sea representado con un logo, escudo, simbolo o algo similar; si no se trata de ese caso, puedes darme el enlace de una imagen que represente o parezca a {prompt_text} o algun tema o topico mas general o padre de este tema que si se pueda representar,los enlaces deben ser de sitios oficiales, wikipedia o alguno de los sitios de las fuentes en donde encontraste las noticias de la pregunta noticias, evita enlaces rotos y fuentes caidas, si no encuentras o no puedes darme el enlace de una imagen, este valor sera nulo
        descripcionComparativa: Traeme una descripcion acerca de la comparativa, que contenga temas relevantes o sucesos que describan las variaciones en los valores comparables de la pregunta comparativa
        Generame un archivo json con la siguiente informacion:
        topic:{prompt_text}
        resumen:Traeme el resumen de una descripcion breve de {prompt_text}
        comparative:texto del csv gererado en la pregunta comparativa en formato de arreglo en vez de separadas las rows por \n cada row sera un arreglo de items de columnas  y el arreglo total sera un arreglo (todo el csv) que contendra arreglos,la primera posicion del arreglo 0 seran los nombres de las columnas del csv, desde la segunda en adelante seran los valores de las columnas del csv
        comparative_variable:el nombre de la variable que se va a usar para generar el grafico comparativo
        image:url de la imagen generada en la pregunta imagen
        news:arreglo clave valor json con la siguiente estructura por cada item generado en la pregunta noticias: path:enlace de la fuente donde encontraste el item de la noticia,valor:texto completo de la noticia generada en la pregunta noticias
        comparative_description:texto de la descripcion generada en la pregunta descripcionComparativa
        colors:un arreglo con 3 colores que tengan referencia al tema de {prompt_text}, que sean brillantes o contrasten bien con un fondo oscuro
        phrase:una frase representativa de {prompt_text}, segundo nombre con el que se conoce a {prompt_text},slogan de {prompt_text},apodo de {prompt_text} o algun dicho 
        popular sobre {prompt_text} o frase popular que represente a {prompt_text} si no la encuentras una frase famosa que tenga referencia al tema de {prompt_text}, selecciona la que mas represente historicamente, que se adapte mas a lo que puede signicar {prompt_text} o que se relacione mas con {prompt_text} ten en cuenta el contexto del tema y que esta frase sea algo que represente de manera general,local,nacional o internacional a {prompt_text}, ten en cuenta popularidad y aceptacion de esta frase en el contexto del topico
        video:traeme el enlace de youtube de un video que haya sido subido recientemente sobre {prompt_text} o algo que represente el tema de {prompt_text} o alguna cosa que sea parecido al tema de {prompt_text}, si no encuentras o no puedes darme el enlace de un video de youtube, este valor sera nulo, buscalo en canales oficiales sobre el tema de {prompt_text}, o en canales muy populares sobre el tema de {prompt_text}
        generame la salida solo con el json, sin ningun tipo de contexto o informacion adicional y la salida debe estar traducida al idioma {self.languajes[self.outputLang]},excepto las claves del json deben estar en ingles tal cual esta en la pregunta y en minusculas
        """
    def setConsult(self,prompt_text):
        prompt_text = self.getPrompt(prompt_text)
        #prompt_text = self.translate(prompt_text)
        ps = subprocess.Popen(('echo', prompt_text), stdout=subprocess.PIPE)
        output = subprocess.check_output(('bito'), stdin=ps.stdout)
        ps.wait()
        output = str(output.decode('UTF-8'))
        #output = self.translate(output,self.outputLang)
        output = output.replace('```json','').replace('```','')
        output = json.loads(output)
        return output
    def getConsult(self):
        text = "```json\n{\n\"topic\": \"Millonarios FC\",\n\"summary\": \"Millonarios FC es un club de fútbol profesional con sede en Bogotá, Colombia, fundado en 1946. Es uno de los equipos más exitosos en la historia del fútbol colombiano, habiendo ganado numerosos títulos de liga y copas nacionales.\",\n\"comparative\": [\n\"Año,Títulos de liga,Copas nacionales,Competiciones internacionales\",\n\"2020,0,0,0\",\n\"2021,1,0,0\",\n\"2022,1,1,0\",\n\"2023,1,0,1\"\n],\n\"variableComparative\": \"Año\",\n\"image\": null\n}\n```"
        return text
    
    def test(self):
        text = self.getConsult()
        text = text.replace('```json','').replace('```','')
        print(text)
        m = json.loads(text)
        print(m)
        return m

    def translate(self,prompt_text,lang='en'):
        print(lang)
        return GoogleTranslator(source='auto', target=lang).translate(prompt_text)