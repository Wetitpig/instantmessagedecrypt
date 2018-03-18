import os
import sys
from hashlib import md5
from subprocess import *
import json


class util:
	bin = "/data/data/com.termux/files/home/"
	encoding = sys.getdefaultencoding()

	def md5sum(text):
			return md5(text.encode(util.encoding))


class param:

	def imei():
		print("Retrieving Device ID...")

		try:
			imei = Popen(["termux-telephony-deviceinfo"], stdout=PIPE)
			imei = json.loads(imei.communicate()[0])
			imei = imei["device_id"]
		except FileNotFoundError:
			print("termux-api Not Installed!")
			exit(1)

		print("Done! Device ID is " + imei)
		return imei

	def uin():
		print("Retrieving UIN...")

		try:
			uin = open("/sdcard/tencent/uin", "r").read()[:-1]
		except OSError:
			print("UIN Not Found!")
			exit(1)

		if util.md5sum("mm" + str(uin)).hexdigest() != param.dir:
			print("Wrong UIN!")
			exit(1)

		print("Done! UIN is " + uin)
		return uin


class decrypt:
		bak = "/dbback/EnMicroMsg.db.bak"
		prefix = "/sdcard/tencent/MicroMsg/"
		sm = "/dbback/EnMicroMsg.db.sm"

		def repair():
			arglist = [util.bin + "dbrepair"]
			arglist.extend(["--verbose"])
			arglist.extend(["--in-key", param.ff])
			arglist.extend(["--output", decrypt.output])
			arglist.extend(["--page-size", "1024"])
			arglist.extend(["--load-master", decrypt.prefix + param.dir + decrypt.sm])
			arglist.extend(["--master-key", param.ff])
			arglist.extend([decrypt.prefix + param.dir + decrypt.bak])

			print("Repairing DB...")

			s = Popen(arglist, stdout = PIPE, stderr = PIPE)
			stdout, stderr = s.communicate()
			print(stdout.decode(util.encoding))
			print(stderr.decode(util.encoding))

		def backup():
			arglist = [util.bin + "dbbackup"]
			arglist.extend(["recover"])
			arglist.extend(["--verbose"])
			arglist.extend(["--key", param.ff])
			arglist.extend(["--output", decrypt.prefix + param.dir + decrypt.bak])
			arglist.extend(["--page-size", "1024"])
			arglist.extend([decrypt.output])

			print("Decrypting DB...")

			b = Popen(arglist, stdout = PIPE, stderr = PIPE)
			stdout, stderr = b.communicate()
			print(stdout.decode(util.encoding))
			print(stderr.decode(util.encoding))


def main(argv):
	if len(argv) == 1:
		decrypt.output = "MicroMsg.db"
	else:
		decrypt.output = argv[1]

	if os.path.isfile(decrypt.output):
		print("Delete old one? (Y/N)")
		ans = input()
		if ans == 'Y' or ans == 'y':
			os.remove(decrypt.output)
		else:
			print("Done!")
			exit(0)

	for param.dir in os.listdir(decrypt.prefix[:-1]):
		if len(param.dir) == 32:
			break

	param.ff = util.md5sum(param.imei() + param.uin()).digest()

	try:
		decrypt.repair()
	except Error as e:
		print(e)
		print("Repair of DB Failed!")
		exit(-1)

	try:
		decrypt.backup()
	except Error as e:
		print(e)
		print("Decryption of DB Failed!")
		exit(-1)

	print("Key: ")
	print(param.ff)


if __name__ == "__main__":
	main(sys.argv)
