# Copyright (c) 2013 Techstorage sp. z o.o.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from tiktalik.error import TiktalikAPIError

from .command import ComputingImageCommand, CommandError


class ListImages(ComputingImageCommand):
    @classmethod
    def add_parser(cls, parent, subparser):
        subparser.add_parser(
            "list-images",
            description="List all available VPS Images.",
            parents=[parent],
        )
        return "list-images"

    def execute(self):
        images = self.conn.list_images()
        for i in images:
            desc = '%s "%s" type=%s' % (i.uuid, i.name, i.type)
            if not i.is_public:
                desc += ", private, %s" % i.create_time
            print(desc)


class RenameImage(ComputingImageCommand):
    @classmethod
    def add_parser(cls, parent, subparser):
        p = subparser.add_parser(
            "rename-image", description="Rename an image.", parents=[parent]
        )
        p.add_argument("uuid", help="Image UUID. This image must belong to you.")
        p.add_argument("name", help="New name for the image.")

        return "rename-image"

    def execute(self):
        try:
            self.conn.rename_image(self.args.uuid, self.args.name)
        except TiktalikAPIError as ex:
            if ex.http_status == 400:
                raise CommandError("Invalid image name")
            elif ex.http_status == 401:
                raise CommandError("User unauthenticated")
            elif ex.http_status == 404:
                raise CommandError("Image doesn't exist in your account")
            raise

        print(("Image %s renamed to %s." % (self.args.uuid, self.args.name)))

class RenameImage(ComputingImageCommand):
    @classmethod
    def add_parser(cls, parent, subparser):
        p = subparser.add_parser("rename-image", description="Rename an image.", parents=[parent])
        p.add_argument("uuid", help="Image UUID. This image must belong to you.")
        p.add_argument("name", help="New name for the image.")

        return "rename-image"

    def execute(self):
        try:
            self.conn.rename_image(self.args.uuid, self.args.name)
        except TiktalikAPIError as ex:
            if ex.http_status == 400:
                raise CommandError("Invalid image name")
            elif ex.http_status == 401:
                raise CommandError("User unauthenticated")
            elif ex.http_status == 404:
                raise CommandError("Image doesn't exist in your account")
            raise

        print("Image %s renamed to %s." % (self.args.uuid, self.args.name))

class DeleteImage(ComputingImageCommand):
    @classmethod
    def add_parser(cls, parent, subparser):
        p = subparser.add_parser(
            "delete-image", description="Delete an image.", parents=[parent]
        )
        p.add_argument("uuid", help="Image UUID. This image must belong to you.")
        p.add_argument(
            "-f", dest="force", action="store_true", help="Don't confirm the action."
        )

        return "delete-image"

    def execute(self):
        confirmed = self.args.force
        if not confirmed:
            confirmed = self.yesno(
                "Are you sure you want to delete image %s?" % self.args.uuid
            )

        if confirmed:
            try:
                self.conn.delete_image(self.args.uuid)
            except TiktalikAPIError as ex:
                if ex.http_status == 404:
                    raise CommandError("Image doesn't exist in your account")
                raise

        print(("Image %s deleted." % self.args.uuid))
