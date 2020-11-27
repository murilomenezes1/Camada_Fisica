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
import datetime
from multiprocessing import Process, Queue

from timeit import default_timer as timer

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"                  # Windows(variacao de)






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


		log = open("client_log.txt","w")
		server_id = 0 
		TIMEOUT = False


		def retry(fun, max_tries=5):
			tentativa = 2 
			for i in range(max_tries):
				print("tentativa numero {}.".format(tentativa))
				print("proxima tentativa em 5 segundos")
				log.write('{} / envio / 5\n'.format(datetime.datetime.now()))
				tentativa+=1
				try:
				   time.sleep(5)

				   fun()
				   break
				except Exception:
					continue
			print("tempo esgotado!")
			

		while comms:

			if STATE == "Start":

				txBuffer0 = open(imageR,'rb').read()
				txSize0 = len(txBuffer0)

				if txSize0 % 114 == 0:
					total_p0 = txSize0//114

				else:
					total_p0 = txSize0//114 + 1
			
				h0 = (1).to_bytes(1, byteorder='big')
				h1 = (0).to_bytes(1, byteorder='big')
				h2 = server_id.to_bytes(1,byteorder='big')
				h3 = total_p0.to_bytes(1,byteorder='big')
				print("payload size ok!")
				h4 = (0).to_bytes(1, byteorder='big')
				print("payload number ok!")
				h5 = (0).to_bytes(1, byteorder='big')
				h6 = (0).to_bytes(1,byteorder='big')
				h7 = (0).to_bytes(1,byteorder='big')
				h8 = (0).to_bytes(1,byteorder='big')
				h9 = (0).to_bytes(1,byteorder='big')
				
				print("total number ok!")

				header = h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7 + h8 + h9

				print("header ok!")
				eop = (0).to_bytes(4,byteorder='big')
				print("eop ok!")
				pkt = header+eop
				print("pkt ok!")
				com.sendData(pkt)
				log.write('{} / envio / 1 / {} / 0 / {}\n'.format(datetime.datetime.now(),txSize0, total_p0))
				print("enviando handshake...")
				print('{} / envio / 1 / {} / 0 / {} - LOGGED'.format(datetime.datetime.now(),txSize0, total_p0))
				STATE = "waiting"

			if STATE == "waiting":

				print("Aguardando resposta do server...")
			

				wait = True



				while wait:

					# rxBuffer,nRx = retry(com.getData(14))
					rxBuffer, nRx = com.getData(14)
					log.write('{} / recebimento / 2 / {}\n'.format(datetime.datetime.now(),len(rxBuffer)))
					if len(rxBuffer) == 14:
						print("Server ativo!")
						STATE = "Connected"
						print("mudando para estado: {}".format(STATE))
						wait = False
						print("wait false")


			if STATE == "Connected" and TIMEOUT == False:

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

				while txSize > 0 and STATE != "Disconnected":

					print("txSize maior que 0")

					if txSize >=114:

						print("fragmentando...")

						h0 = (3).to_bytes(1, byteorder='big')
						h1 = (0).to_bytes(1, byteorder='big')
						h2 = server_id.to_bytes(1, byteorder='big')
						h3 = (total_p).to_bytes(1,byteorder='big')
						h4 = (current_p).to_bytes(1, byteorder='big')
						h5 = (114).to_bytes(1, byteorder='big')
						h6 = (current_p).to_bytes(1,byteorder='big')
						h7 = (current_p-1).to_bytes(1,byteorder='big')
						h8 = (0).to_bytes(1,byteorder='big')
						h9 = (0).to_bytes(1,byteorder='big')

						

						header = h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7 + h8 + h9
						print("header ok!")
						payload = txBuffer[i:i+114]
						print("payload ok!")
						eop2 = (0).to_bytes(4,byteorder='big')
						pkt2 = header + payload + eop2


						com.sendData(pkt2)
						log.write('{} / envio / 3 / {} / {} / 0 / {}\n'.format(datetime.datetime.now(),txSize, current_p, total_p))
						print('{} / envio / 3 / {} / {} / 0 / {} - LOGGED'.format(datetime.datetime.now(),txSize, current_p, total_p))
						# com.sendData(header)
						# print("header enviado")
						# com.sendData(payload)
						# print("payload enviado")
						# com.sendData(eop2)
						# print("eop enviado")

						print("pacote enviado...")


						time.sleep(0.1)
						HeaderRespostaServer, HeaderRxBuffer = com.getData(10)
						log.write('{} / recebimento / 4 / {}\n'.format(datetime.datetime.now(),len(HeaderRespostaServer)))
						print('{} / recebimento / 4 / {}\n'.format(datetime.datetime.now(),len(HeaderRespostaServer)))

						if HeaderRespostaServer == "TIMEOUT":

							print("TIMEOUT")
							h0 = (5).to_bytes(1, byteorder='big')
							h1 = (0).to_bytes(1, byteorder='big')
							h2 = (0).to_bytes(1, byteorder='big')
							h3 = (0).to_bytes(1,byteorder='big')
							h4 = (0).to_bytes(1, byteorder='big')
							h5 = (0).to_bytes(1, byteorder='big')
							h6 = (0).to_bytes(1,byteorder='big')
							h7 = (0).to_bytes(1,byteorder='big')
							h8 = (0).to_bytes(1,byteorder='big')
							h9 = (0).to_bytes(1,byteorder='big')

							pkt_timeout = h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7 + h8 + h9 + EopRespostaServer
							print("Timeout package ok!")

							# com.sendData(pkt_timeout)
							log.write("{} / envio / 5\n".format(datetime.datetime.now()))
							print(("{} / 5 - LOGGED".format(datetime.datetime.now())))

							TIMEOUT = True
							print("TIMEOUT TRUE")
							# com.disable()
							# print("COM DISABLED.")
							STATE = "Disconnected"
							print("mudando para estado DISCONNECTED")
							comms = False
							

						else:	
							


							EopRespostaServer, EopRxBuffer = com.getData(4)

							log.write('{} / recebimento / 4 / {}\n'.format(datetime.datetime.now(),len(EopRespostaServer)))
							print('{} / recebimento / 4 / {}\n'.format(datetime.datetime.now(),len(EopRespostaServer)))

							if EopRespostaServer == eop2:

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


						h0 = (3).to_bytes(1, byteorder='big')
						h1 = (0).to_bytes(1, byteorder='big')
						h2 = server_id.to_bytes(1, byteorder='big')
						h3 = (total_p).to_bytes(1,byteorder='big')
						h4 = (current_p).to_bytes(1, byteorder='big')
						h5 = txSize.to_bytes(1, byteorder='big')
						h6 = (current_p).to_bytes(1,byteorder='big')
						h7 = (current_p-1).to_bytes(1,byteorder='big')
						h8 = (0).to_bytes(1,byteorder='big')
						h9 = (0).to_bytes(1,byteorder='big')


						header = h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7 + h8 + h9
						print("header ok")

						payload = txBuffer[i:]
						print("payload ok")
						eop2 = (0).to_bytes(4,byteorder='big')
						print("eop ok")
						pkt2 = header + payload + eop2
						print("pkt ok")

						com.sendData(pkt2)
						log.write('{} / envio / 3 / {} / {} / 0 / {}\n'.format(datetime.datetime.now(),txSize, current_p, total_p))
						print('{} / envio / 3 / {} / {} / 0 / {} - LOGGED'.format(datetime.datetime.now(),txSize, current_p, total_p))

						print("ultimo pacote enviado.")

						comms = False

						STATE = "End"
						break



		if STATE == "Disconnected":

			print("Tempo esgotado! encerrando...")
			log.close()
			com.disable()
			
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

			log.close()
			print('Taxa de transferencia: {} bytes por segundo' .format(txtrans))
			print("-------------------------")
			print("Comunicação encerrada")
			print("-------------------------")
			com.disable()
	except:
		log.close()
		
		print("ops! :-\\")
		print("-------------------------")
		print(" fechando log...")
		com.disable()

	#so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
	main()