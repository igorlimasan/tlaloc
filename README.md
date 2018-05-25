# Tlaloc
     ---
    
```
    Servidor: ---
    Status: Desenvolvimento
```

Pacote com ferramentas de interpolação utilizadas pela Climatempo.
#### Tecnologias:
* Python 3.6.1
 >  * [Argparse] 1.*
 > * [Pandas]

### Configuração de inicialização:
Os arquivos de configuração contem as informações para a coleta dos dados.
Os arquivos ficam no diretorio 'tlaloc' no formato json:
```sh
$ ls /work/tlaloc/tlaloc/
```
        


#### service.py:
O *service* e responsável por entregar as funcionalidades desenvolvidas, o arquivo
esta na raiz do projeto. Utilizar o parâmetro -h ou --help para descobrir as opções de conforme o exemplo:

```bash
$ .../tlaloc/service.py --help
$ .../tlaloc/service.py --configure .../tlaloc/tlaloc/configure.json
```  


#### Arquivos de Entrada:
O projeto suporta arquivos CSV como entrada, desde que no arquivo de configuração os campos correspondentes sejam inseridos corretamente

```bash
$ .../tlaloc/service.py --help
$ .../tlaloc/service.py --configure .../tlaloc/tlaloc/configure.json -f .../path_to_file/file.csv
```

[Argparse]: <https://docs.python.org/2/howto/argparse.html>
[Pandas]: <http://pandas.pydata.org/>
