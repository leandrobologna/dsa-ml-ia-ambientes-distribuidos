# Exemplos em Pyspark
### Criando uma lista no pyspark
palavras = ['apache', 'spark', 'open-source', 'framework']

### Criando uma parallelize collection para possibilitar a execução da lista acima de forma distribuida
distributed_palavras = sc.parallelize(palavras)

## Executando operaçãos nos objetos paralelizados
### Filtrando o Objeto
filtro_palavras = distributed_palavras.filter(lambda x: len(x) > 5)

### Realizando um Count no Objeto
filtro_palavras.count()

### Criando um Dataset Distribuído
#### Crie um arquivo com texto


### Crie um dataset em pyspark
local_file = sc.textFile("teste.txt")

### Realizando um count no arquivo
local_file.count()

### Realizando um filtro no aurquivo
local_file.filter(lambda x: len(x) > 3).count()