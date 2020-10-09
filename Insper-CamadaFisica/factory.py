def header(payload,current_p, total_p):

    print("montando header")

    payload_size = (payload).to_bytes(4, byteorder='big')

    print("payload size ok!")
    payload_number = current_p.to_bytes(2, byteorder='big')
    print("payload number ok!")
    total_number = total_p.to_bytes(4,byteorder='big')
    print("total number ok!")

    header = payload_size + payload_number + total_number

    return header