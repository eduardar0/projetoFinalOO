from datarecord import DataRecord

data_record = DataRecord()
session_id = data_record.checkUser('Eduarda', '111')
if session_id: 
    print(session_id)
    print("usuario autenticado")
else: 
    print("usuario nao encotrado")

banco = data_record.get_tasks(session_id)
print(banco)

#export PYTHONPATH=/mnt/c/Users/Joelma/Documents/bonusPF/bmvc


