import pymysql
def getdbcur():
    conn = pymysql.connect(host='warehouse.cnao4tphciap.ap-south-1.rds.amazonaws.com',
                                                port = 3306,
                                                user = 'admin',
                                                passwd = 'umeshkv2',
                                                db = 'warehouse',
                                                autocommit = True)
    cur = conn.cursor()
    return cur