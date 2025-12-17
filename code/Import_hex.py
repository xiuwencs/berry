from scapy.all import *
import csv

def Non_deal(df):
    list_data = []
    rows = len(df)
    for i in range(0, rows):
        list = df[i]
        list_con = []
        cols = len(list)
        for j in range(0, cols):
            if list[j] != "nan":
                list_con.append(list[j])  # 如果用remove法需要倒序去除，否则无法去除干净（因为每一次去除会导致len-1)
        list_data.append(list_con)
    return list_data

def export_pcapng_to_hex(pcapng_file, output_file):
    packets = rdpcap(pcapng_file)  # 读取pcapng文件
    with open(output_file, 'w') as file:
        for packet in packets:
            hexdump = ','.join([f"{byte:02x}" for byte in bytes(packet)])  # 将数据包转换为十六进制表示，并用逗号分隔每个字节
            file.write(hexdump + '\n')  # 将十六进制表示写入文件，每行一个协议

    print("导出完成！")

def import_file(pcapng_file, output_file):
    export_pcapng_to_hex(pcapng_file, output_file)
    # 数据导入
    header = ['{}'.format(i) for i in range(0, 1460)]
    # 创建csv文件并写入表头
    with open(output_file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = [row for row in reader]
    data.insert(0, header)
    # 写入新的csv文件
    with open('new.txt', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

    with open('new.txt', 'r')as file:
        reader = csv.reader(file)
        next(reader)
        data = list(reader)
    data = Non_deal(data)
    if output_file == 'modbus':
        data = [row[66:] for row in data]
    elif output_file == 'icmp':
        data = [row[38:] for row in data]
    elif output_file == 'smb':
        data = [row[62:] for row in data]
    elif output_file == 'modbus_100':
        data = [row[54:] for row in data]
    elif output_file == 'icmp_100':
        data = [row[38:] for row in data]
    elif output_file == 'smb_100':
        data = [row[62:] for row in data]
    elif output_file == 'coap':
        data = [row[44:] for row in data]
    elif output_file == 'dns':
        data = [row[28:] for row in data]
    elif output_file == 'gh0st':
        data = [row[54:] for row in data]
    elif output_file == 'mqtt':
        data = [row[68:] for row in data]
    elif output_file == 'nbns10000':
        data = [row[46:] for row in data]
    elif output_file == 'qq5':
        data = [row[42:] for row in data]
    elif output_file == 'snmp':
        data = [row[44:] for row in data]
    elif output_file == 'stun':
        data = [row[42:] for row in data]
    elif output_file == 'tls':
        data = [row[54:] for row in data]
    elif output_file == 'Websoc_all':
        data = [row[54:] for row in data]
    elif output_file == 'rtp':
        data = [row[42:] for row in data]
    return data


