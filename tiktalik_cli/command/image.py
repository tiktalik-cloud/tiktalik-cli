from tiktalik.error import TiktalikAPIError

from .command import Command

class ListImages(Command):
	@classmethod
	def add_parser(cls, parent, subparser):
		subparser.add_parser("list-images", description="List all available VPS Images.", parents=[parent])
		return "list-images"

	def execute(self):
		images = self.conn.list_images()
		for i in images:
			print '%s "%s", type=%s %s' % (i.uuid, i.name, i.type, "(private)" if not i.is_public else "")


class DeleteImage(Command):
	@classmethod
	def add_parser(cls, parent, subparser):
		p = subparser.add_parser("delete-image", description="Delete an image.", parents=[parent])
		p.add_argument("uuid", help="Image UUID. This image must belong to you.")
		p.add_argument("-f", dest="force", action="store_true", help="Don't confirm the action.")

		return "delete-image"

	def execute(self):
		confirmed = self.args.force
		if not confirmed:
			confirmed = self.yesno("Are you sure you want to delete image %s?" % self.args.uuid)

		if confirmed:
			try:
				self.conn.delete_image(self.args.uuid)
			except TiktalikAPIError as ex:
				if ex.http_status == 404:
					raise CommandError("Image doesn't exist in your account")
				raise

		print "Image %s deleted." % self.args.uuid
