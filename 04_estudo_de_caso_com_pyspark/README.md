# Ajustando os Parâmetros de Memória do PySpark
>**Observação:**
> Essas configurações devem ser realizadas em todas os nós do cluster SPARK
#### Acesse a pasta conf do spark.
~~~
cd /opt/spark/conf
~~~

#### Crie uma cópia do arquivo **spark-defaults.conf**.
~~~
cp spark-defaults.conf.template spark-defaults.conf
~~~

#### Edite o arquivo **spark-defaults.conf**.
> **Observação:**
> Os parâmetros para serem atualizados são o spark.driver.memory caso as limitações de memória de sua máquina seja abaixo da configuração padrão de 5g, e o spark.local.dir com o diretório temporário /tmp para o spark salvar as execuções temporárias.
~~~
vi spark-defaults.conf
~~~

#### Altere o parâmetro **soft** e **hard** do  SO na pasta limits.conf, para alterar os limites do SO.
~~~
cd ~
sudo vi /etc/security/limits.conf
~~~

#### A forma como o arquivo limits.conf deve ficar é igual a imagem abaixo.
![](/dsa-ml-ia-ambientes-distribuidos/04_estudo_de_caso_com_pyspark/imgs/etapa-1-use-case.PNG)

#### Inicialize o Spark Cluster
~~~
# Acesse a pasta sbin do Spark
cd /opt/spark/sbin

# Inicialize o servidor
./start-all.sh
~~~

## Configurando o Acesso Remoto ao Cluster a partir da Máquina Local
> **Observação**:
> 
> Para dar continuidade no projeto que iremos realizar teremos que configurar a máquina local para realizar o acesso remoto ao servidor, ou seja, não iremos executar as atividades do projeto no cluster diretamente e sim na máquina local com acesso remoto ao cluster criado.
> 
> Para isso precisamos realizar as configurações do Java JDK 1.8, Apache Spark 3.2.1 e Anaconda3 na máquina local como feito nas atividades anteriores.
>
> Para estas aulas eu estou utilizando o subsistema Ubuntu, no qual, irei instalar todos as aplicações instaladas anteriormente. Para realizar a instalação do Ubuntu a partir do WSL siga as instruções passadas neste link: https://docs.microsoft.com/pt-br/windows/wsl/install

#### Realize a atualização do pacote apt, conforme abaixo.
~~~
sudo apt update
~~~

#### Acesse a pasta */opt*.
~~~
cd /opt
~~~
### **Realizando a instalação do Java JDK 1.8**
#### Realize o Download do Java JDK 1.8
~~~
# Download do Java JDK 1.8
wget http://datascienceacademy.com.br/blog/aluno/JDK/jdk-8u181-linux-x64.tar.gz

# Caso o wget não esteja instalado siga a instrução abaixo antes de realizar o download.
sudo apt install wget
~~~

#### Descompacte o arquivo dentro da pasta */opt*.
~~~
tar xzfv jdk-8u181-linux-x64.tar.gz
~~~

#### Renomeie a pasta *jdk1.8.0_181* para *jdk*.
~~~
mv jdk1.8.0_181/ jdk
~~~

#### Remova o **TARBALL** para limpar o disco e manter ele organizado.
~~~
rm -r jdk-8u181-linux-x64.tar.gz
~~~

#### Realize a inclusão do Java JDK 1.8 no arquivo *.profile*.
~~~
# Acesse a pasta raiz
cd ~

# Acesse o arquivo .profile
sudo vi .profile

### Inclua os comandos abaixo dentro do arquivo .profile
# Java JDK 1.8
export JAVA_HOME=/opt/jdk
export JRE_HOME=/opt/jdk/jre
export PATH=$PATH:$JAVA_HOME/bin:$JRE_HOME/bin

# Atualize as variáveis de ambiente
source .profile
~~~

#### Verefique a versão do Java JDK instalada
~~~
java -version
~~~

#### A saida dever parecida com a imagem abaixo.
![](/dsa-ml-ia-ambientes-distribuidos/04_estudo_de_caso_com_pyspark/imgs/etapa-2-use-case.PNG)

### **Realizando a instalação do Apache Spark 3.2.1**
#### Acesse a pasta */opt*.
~~~
cd /opt
~~~

#### Realize o download do Apache Spark.
~~~
wget https://archive.apache.org/dist/spark/spark-3.2.1/spark-3.2.1-bin-hadoop3.2.tgz
~~~

#### Descompacte o TARBALL do Apache Spark.
~~~
sudo tar xzvf spark-3.2.1-bin-hadoop3.2.tgz
~~~

#### Remova o TARBALL do Apache Spark.
~~~
sudo rm -r spark-3.2.1-bin-hadoop3.2.tgz
~~~

#### Renomeie o *spark-3.2.1-bin-hadoop3.2* para *spark*.
~~~
sudo mv spark-3.2.1-bin-hadoop3.2/ spark
~~~

#### Inclua o spark nas varivéis de ambiente.
~~~
# Retorne para a pasta raiz
cd 

# Acesse o arquivo .profile e inclua no final dele as variáveis de ambiente do spark conforme abaixo
sudo vi .profile

# Spark 3.2.1
export SPARK_HOME=/opt/spark
export PATH=$PATH:$SPARK_HOME/bin

# Atualize as variáveis de ambiente
source .profile
~~~

#### Teste o spark
~~~
spark-shell
~~~

#### A saída do console deve ser algo parecido com a imagem abaixo
![](/dsa-ml-ia-ambientes-distribuidos/04_estudo_de_caso_com_pyspark/imgs/etapa-3-use-case.PNG)

### **Realizando a Instalação do Anaconda 3**
#### Crie a pasta Downloads caso não tenha e a acesse
~~~
# Acessando a pasta raiz
cd 

# Criar a pasta Downloads
mkdir Downloads

# Acesse a pasta Downloads
cd Downloads/
~~~

#### Realize o Download o Script Bash do Anaconda 3
~~~
wget https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh
~~~

#### Realize a Instalação do Anaconda 3 seguindo as Instruções Padrões de Instalação
~~~
bash Anaconda3-2022.05-Linux-x86_64.sh
~~~

#### Atualize as Variáveis de Ambiente
~~~
source .bashrc
~~~

#### Teste o PySpark para Verificar se o Pyspark está Enxergando a Versão do Python do Anaconda3
~~~
pyspark
~~~

#### A Saída do Console deve ser Semelhante ao da Imagem Abaixo.
![](/dsa-ml-ia-ambientes-distribuidos/04_estudo_de_caso_com_pyspark/imgs/etapa-4-use-case.PNG)

### **Realizar a Conexão da Máquina Local a Partir do Pyspark**
#### Para Realizar a Conexão ao PySPark a parti da máquina local faça conforme imagem abaixo, troque apenas o IP que será diferente.
~~~
# Acesse a pasta onde estão os arquivos do Projeto e execute o comando abaixo
pyspark --master spark://192.168.15.134:7077
~~~

> **Observação:**
>
> Caso ocorra problemas de comunicação verifique se a porta 7077 está habilitada para conexão, caso não esteja libere o firewall para essa porta do node master.