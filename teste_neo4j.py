from myneo4j import driver

driver.verify_connectivity()
print("Conectado ao Neo4j!")

registros, resumo, chaves = driver.execute_query("RETURN 'Olá, Neo4j' AS mensagem")
print(registros[0]["mensagem"])

driver.close()
