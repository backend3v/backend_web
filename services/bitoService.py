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
        noticias:Traeme las 3 noticias mas importantes actualmente sobre {prompt_text} tienen que ser noticias relevantes y no mas antiguas de 1 semana de preferencia noticias que hayan sido polemicas, importantes y relevantes para {prompt_text}, buscalas de fuentes oficiales y evita en lo posible fake news y fuentes de dudosa procedencia
        comparativa:hazme un csv con campos que se puedan usar para generar un grafico comparativo, busca valores comparables puede ser entre tiempo,region,items afines o contrarios, algun contexto sobre las noticias generadas o otros factores que puedan ser relevantes; sobre el tema de {prompt_text}
        imagen:Traeme una imagen acerca de {prompt_text}, si se trata de una organizacion, empresa, institucion o algo que sea representado con un logo, escudo, simbolo o algo similar; si no se trata de ese caso, puedes darme el enlace de una imagen que represente o parezca a {prompt_text} o algun tema o topico mas general o padre de este tema que si se pueda representar, si no encuentras o no puedes darme el enlace de una imagen, este valor sera nulo
        descripcionComparativa: Traeme una descripcion acerca de la comparativa, que contenga temas relevantes o sucesos que describan las variaciones en los valores comparables de la pregunta comparativa
        Generame un archivo json con la siguiente informacion:
        topic:{prompt_text}
        resumen:Traeme el resumen de una descripcion breve de {prompt_text}
        comparative:texto del csv gererado en la pregunta comparativa en formato de arreglo en vez de separadas las rows por \n cada row sera un arreglo de items de columnas  y el arreglo total sera un arreglo (todo el csv) que contendra arreglos (cada row) que contendran items (cada columna), la primera 
        columna debe ser la variable que se va a usar para generar el grafico comparativo, las siguientes columnas deben ser los valores comparables
        variacompaative_variable:bleComparativa:el nombre de la variable que se va a usar para generar el grafico comparativo
        image:url de la imagen generada en la pregunta imagen
        news:arreglo clave valor json con la siguiente estructura por cada item generado en la pregunta noticias: path:enlace de la noticia,valor:texto de la noticia
        compaative_description:texto de la descripcion generada en la pregunta descripcionComparativa
        generame la salida solo con el json, sin ningun tipo de contexto o informacion adicional y la salida debe estar traducida al idioma {self.languajes[self.outputLang]},excepto las claves del json deben estar en ingles tal cual esta en la pregunta y en minusculas
        """
    def setConsult(self,prompt_text):
        prompt_text = self.getPrompt(prompt_text)
        prompt_text = self.translate(prompt_text)
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