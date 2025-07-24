import subprocess,json,re
from deep_translator import GoogleTranslator
import os
from jinja2 import Template

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
        # Leer el template desde archivo y renderizar con Jinja2
        template_path = os.path.join(os.path.dirname(__file__), 'bito_prompt_template.txt')
        with open(template_path, 'r', encoding='utf-8') as f:
            template_str = f.read()
        template = Template(template_str)
        prompt = template.render(prompt_text=prompt_text, lang=self.languajes[self.outputLang])
        return prompt
    def setConsult(self,prompt_text):
        prompt_text = self.getPrompt(prompt_text)
        ps = subprocess.Popen(('echo', prompt_text), stdout=subprocess.PIPE)
        output = subprocess.check_output(('bito'), stdin=ps.stdout)
        ps.wait()
        output = str(output.decode('UTF-8'))
        output = output.replace('```json','').replace('```','')
        output = json.loads(output)
        return output
    def getConsult(self):
        # Leer el ejemplo de respuesta desde archivo JSON
        import json, os
        example_path = os.path.join(os.path.dirname(__file__), 'bito_example_response.json')
        with open(example_path, 'r', encoding='utf-8') as f:
            example = json.load(f)
        return example
    def test(self):
        text = self.getConsult()
        print(text)
        return text
    def translate(self,prompt_text,lang='en'):
        print(lang)
        return GoogleTranslator(source='auto', target=lang).translate(prompt_text)