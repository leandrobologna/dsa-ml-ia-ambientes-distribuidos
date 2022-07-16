# **Preparando o Ambiente Pyspark**

Para conseguirmos dar continuidade no curso de Machine Learning e Inteligência Artificial em Ambientes Distribuídos do Data Science Academy (DSA), precisamos realizar o resto das configurações para que o PySpark (Python com Spark) funcione. 

Para realizar as configurações basta seguir as instruções abaixo.

# Instalando o Anaconda
Para realizar a instalação do Anaconda realize os comandos abaixo.
~~~
# Acesse a pasta de Downloads
cd Downloads

# Baixe o arquivo BASH do anaconda
sudo wget https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh

# Execute a instalação seguindo as instruções
bash Anaconda3-2022.05-Linux-x86_64.sh

# Confirma a inclusão do Anaconda dentro das variáveis de ambiente
source .bashrc
~~~

Verifique se o pyspark está com a versão Python do Anaconda.
~~~
pyspark
~~~

A saída do console deve ser algo parecido com a imagem abaixo.
![](/dsa-ml-ia-ambientes-distribuidos/03_introducao_apache_spark/imgs/etapa-1-config-pyspark.PNG)