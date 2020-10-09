#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import * 
import time

from timeit import default_timer as timer

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM1"                  # Windows(variacao de)




 
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




def main():
	try:
		
		com = enlace(serialName)
	
		# Ativa comunicacao. Inicia os threads e a comunicação seiral 
		# com.enable()
		# print("comunicação aberta com sucesso. porta {}".format(serialName))
	
		imageR = input("digite o PATH da imagem (ex: insper.png): ") #"insper.png"
		req = input("iniciar comunicação? [s/n]: ")


		if req == "s":
			comms = True
			STATE = "Start"
			com.enable()
			print("comunicação aberta com sucesso. porta {}".format(serialName))

		while comms:

			if STATE == "Start":
				print("Iniciando...")
				# header1 = header(255,0,0)
				payload_size = (1).to_bytes(4, byteorder='big')
				print("payload size ok!")
				payload_number = (0).to_bytes(2, byteorder='big')
				print("payload number ok!")
				total_number = (0).to_bytes(4,byteorder='big')
				print("total number ok!")

				header = payload_size + payload_number + total_number

				print("header ok!")
				eop = (0).to_bytes(4,byteorder='big')
				print("eop ok!")
				pkt = header+eop
				print("pkt ok!")
				com.sendData(pkt)
				print("enviando handshake...")
				STATE = "waiting"

			if STATE == "waiting":

				print("Aguardando resposta do server...")

				hst = time.time()
				wait = True

				while wait:

					rxBuffer,nRx = com.getData(14)
					if len(rxBuffer) == 14:
						print("Server ativo!")
						STATE = "Connected"
						print("mudando para estado: {}".format(STATE))
						wait = False
						print("wait false")

					het = time.time()
					dht = hst - het

					if dht > 5:
						wait = False  
						retry = input("Server inativo. tentar novamente? [s/n]: ")
						if retry == "s":
							STATE = "Start"

						elif retry == "n":
							print("Encerrando")
						
							break

			if STATE == "Connected":

				print("Conectando...")

				start = timer()
				print("timer iniciado.")
				txBuffer = open(imageR,'rb').read()
				print("imagem lida com sucesso.")
				txSize = len(txBuffer)

				print("Tamanho txBuffer: {}".format(txSize))


				if txSize % 114 == 0:
					total_p = txSize//114

				else:
					total_p = txSize//114 + 1

				print("total de pacotes: {}".format(total_p))

				current_p = 1
				i = 0 
				p_left = total_p
				pacotes_enviados = 0

				while txSize > 0:

					print("txSize maior que 0")

					if txSize >=114:

						print("fragmentando...")

						payload_size = (114).to_bytes(1, byteorder='big')
						print("payload size ok!")
						payload_number = (current_p).to_bytes(1, byteorder='big')
						print("payload number ok!")
						total_number = (total_p).to_bytes(1,byteorder='big')
						print("total number ok!")
						h3 = (0).to_bytes(1,byteorder='big')
						h4 = (0).to_bytes(1,byteorder='big')
						h5 = (0).to_bytes(1,byteorder='big')
						h6 = (0).to_bytes(1,byteorder='big')
						h7 = (0).to_bytes(1,byteorder='big')
						h8 = (0).to_bytes(1,byteorder='big')
						h9 = (0).to_bytes(1,byteorder='big')

						

						header = payload_size + payload_number + total_number + h3 + h4 + h5 + h6 + h7 + h8 + h9
						print("header ok!")
						payload = txBuffer[i:i+115]
						print("payload ok!")
						eop2 = (0).to_bytes(4,byteorder='big')
						pkt2 = header + payload + eop2


						com.sendData(pkt2)
						# com.sendData(header)
						# print("header enviado")
						# com.sendData(payload)
						# print("payload enviado")
						# com.sendData(eop2)
						# print("eop enviado")

						print("pacote enviado...")


						time.sleep(0.1)
						respostaServer, rxBuffer = com.getData(4)

						if respostaServer == eop2:

							current_p += 1
							i += 114
							txSize -= 114
							p_left -= 1
							pacotes_enviados += 1
						else:

							print("Erro! Eop na posicao errada. Tamanho de payload incorreto")


						print("Pacote Atual: {}".format(current_p))
						print("Tamanho restante: {}".format(txSize))
						# print("Numero de pacotes restantes: {}".format(total_p-current_p))
						print("pacotes enviados: {}".format(pacotes_enviados))

					else:


						payload_size = txSize.to_bytes(1, byteorder='big')
						print("payload size ok!")
						payload_number = (current_p).to_bytes(1, byteorder='big')
						print("payload number ok!")
						total_number = (total_p).to_bytes(1,byteorder='big')
						print("total number ok!")
						h3 = (0).to_bytes(1,byteorder='big')
						h4 = (0).to_bytes(1,byteorder='big')
						h5 = (0).to_bytes(1,byteorder='big')
						h6 = (0).to_bytes(1,byteorder='big')
						h7 = (0).to_bytes(1,byteorder='big')
						h8 = (0).to_bytes(1,byteorder='big')
						h9 = (0).to_bytes(1,byteorder='big')


						header = payload_size + payload_number + total_number + h3 + h4 + h5 + h6 + h7 + h8 + h9
						print("header ok")

						payload = txBuffer[i:]
						print("payload ok")
						eop2 = (0).to_bytes(4,byteorder='big')
						print("eop ok")
						pkt2 = header + payload + eop2
						print("pkt ok")

						com.sendData(pkt2)
						print("ultimo pacote enviado.")

						comms = False

						STATE = "End"
						break




		if STATE == "End":

			# bytesize = (txSize).to_bytes(4, byteorder='big')
			# com.sendData(bytesize)  
			# time.sleep(0.1)
			# com.sendData(txBuffer)
			# time.sleep(0.1)
			# respostaServer, rxBuffer = com.getData(4)
			print("imagem enviada com sucesso.")
	
			# if respostaServer == bytesize:
			#     print("sucesso!")
			# Encerra comunicação
			print("-------------------------")

			rxBuffer, nRx = com.getData(1)
			print("resposta final recebida.")

			confirm = int.from_bytes(rxBuffer, byteorder='big')

			if confirm == 0:
				print("Sucesso!")
			
			end = timer()
			delta_t = end - start
			txtrans = txSize/delta_t
			print('Taxa de transferencia: {} bytes por segundo' .format(txtrans))
			print("-------------------------")
			print("Comunicação encerrada")
			print("-------------------------")
			com.disable()
	except:
		print("ops! :-\\")
		com.disable()

	#so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
	main()