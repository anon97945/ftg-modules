from .. import loader, utils
from typing import Union
import os
import asyncio
import time
from glitch_this import ImageGlitcher
from PIL import Image


def register(cb):
    cb(GlitchMod)

class GlitchMod(loader.Module):
    """ Create Glitch effect in pic or gif """
    strings = {
        'name': 'Glitch',
        'media_not_found': 'Media not found',
        'invalid_input': 'Your input is invalid',
        'processing': '<b>Glitching...</b>',
        'img_required': 'I need image',
        'out_of_range': 'input out of range, must be > 0 < 10'
    }
    type_gif = "gif"
    type_pic = "png"

    def __init__(self):
        self.name = self.strings['name']

    async def client_ready(self, client, db):
        self.client = client
        self._db = db

    async def gchcmd(self, message):
        """.gch <strength> <g (optional, if true then generates a gif >"""
        replied = await message.get_reply_message()
        args = utils.get_args(message)
        input_ = 3
        if args:
            if args[0].isdigit():
                input_ = int(args[0])
                if input_ < 0 or input_ > 9:
                    await message.edit(self.strings['out_of_range'])
                    return
        if not (replied and (
            replied.photo or replied.sticker or replied.gif)):
            await message.edit(self.strings['media_not_found'])
            return
        if replied.file.ext == '.tgs':
            await message.edit(self.strings['media_not_found'])
            return
        await message.edit(self.strings['processing'])
        ext = ".gif" if "g" in args else ".png"
        file_to_process = await self.client.download_media(replied, 'to_glitch' + ext)
        self.glitcher = ImageGlitcher()
        glitched = self.glitch(str(file_to_process), input_, ext[1:])
        await self.client.send_file(message.to_id, glitched)
        await message.delete()
        os.remove(glitched)
        os.remove(file_to_process)
    
        
    def glitch(self,filename: str, range_:int, glitch_type: str) -> str:
        """ returns filename of glitched gif/pic """
        img = Image.open(filename)
        glitched_filename = "glitched_" + filename
        if glitch_type == self.type_gif:
            return self.glitch_to_gif(img, range_, glitched_filename)
        elif glitch_type == self.type_pic:
            return self.glitch_img(img, range_, glitched_filename)

    def glitch_img(self, img: Image.Image, range_: int, output_filename: str) -> str:
        """ glitches img file with [filename] and returns glitched image name """
        glitch_img = self.glitcher.glitch_image(img, range_, color_offset=True)
        glitch_img.save(output_filename)
        return output_filename
    
    def glitch_to_gif(self, img: Image.Image, range_: int, output_filename: str) -> str:
        """ glitches img file and returns glitched GIF name """
        DURATION = 200
        LOOP = 0
        glitch_img = self.glitcher.glitch_image(img, range_, color_offset=True, gif=True)
        glitch_img[0].save(
            output_filename,
            format="GIF",
            append_images=glitch_img[1:],
            save_all=True,
            duration=DURATION,
            loop=LOOP,
        )
        return output_filename
