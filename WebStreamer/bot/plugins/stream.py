# This file is a part of TG-FileStreamBot
# Coding : Jyothis Jayanth [@EverythingSuckz]

from pyrogram import filters
from WebStreamer.vars import Var
from urllib.parse import quote_plus
from WebStreamer.bot import StreamBot
from pyrogram.types.messages_and_media import message
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import requests
import psycopg2

API_S= Var.API_SB
BASE_URL="https://api.streamsb.com/api/upload/url?key="+API_S+"&url="
STREAMSB_URL="https://embedsb.com/"
DROP_URL="https://droplink.co/api?api=d61f38da5372ed4c13655f94ee3564b20f6fd525&url="
GP_LINK="https://gplinks.in/api?api=ceb30468694ff94f00f40127cee2c2223d39d42a&url="
URL_PAY="https://urlpayout.com/api?api=e046f40953ff16b030afe058fed310da2505412f&url="
def detect_type(m: Message):
    if m.document:
        return m.document
    elif m.video:
        return m.video
    elif m.audio:
        return m.audio
    else:
        return
    

@StreamBot.on_message(filters.private & (filters.document | filters.video | filters.audio), group=4)
async def media_receive_handler(_, m: Message):
    file = detect_type(m)
    file_name = ''
    if file:
        file_name = file.file_name
        log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)
        

    stream_link = Var.URL  + str(log_msg.message_id) + '/' +quote_plus(file_name) if file_name else ''
    response= requests.get(BASE_URL+stream_link)  
    final_sb_url =STREAMSB_URL+response.json().get("result").get("filecode")+".html" 
    filecode=response.json().get("result").get("filecode")
    file_name_api=file_name.replace("@","").replace(".","").replace("_","").replace("-","").replace(" ","").replace("x","")
    
    conn = psycopg2.connect("host=1de65d0c-8d0e-4572-bb1d-c94dfabffd41.gcp.ybdb.io port=5433 dbname=yugabyte user=showflix password=srimaniSRI-98") 
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    
    
    response2= requests.get(DROP_URL+final_sb_url+"&alias=showflixfile-"+filecode)
    response3= requests.get(GP_LINK+final_sb_url+"&alias=showflixfile-"+filecode)
    response4= requests.get(URL_PAY+final_sb_url+"&alias=showflixfile-"+filecode)
    
    final_drop_url=response2.json().get("shortenedUrl")
    final_gp_link=response3.json().get("shortenedUrl")
    final_url_pay=response4.json().get("shortenedUrl")
    
    file_name=file_name.replace("@"," ").replace("."," ").replace("_"," ").replace("-"," ").replace("+"," ")
    
    insertstring="""INSERT INTO streamsb(moviename,streamsblink,droplink,gplink,urlpayoutlink) VALUES(%s,%s,%s,%s,%s)"""
    recordstoinsert=(file_name,final_sb_url,final_drop_url,final_gp_link,final_url_pay)
    
    cur.execute(insertstring,recordstoinsert)
    
    cur.close()
    conn.close()
    
    print(final_drop_url)
    
    
    await m.reply_text(
        text=f"<b>🎬 Movie Name: </b>  ```{file_name}```\n\n" f"<b>🔗  Link 1: {final_drop_url}</b>\n\n" f"<b>🔗  Link 2: {final_gp_link} </b>\n\n" f"<b>🔗  Link 3: {final_url_pay}</b>\n\n" f"<b>🔗  Link 4:{final_sb_url}</b>\n\n"  f"<b>📤 Uploaded by :</b> ██▓▒░⡷⠂𝚂𝙷𝙾𝚆𝙵𝙻𝙸𝚇⠐⢾░▒▓██\n\n" f"<b>📥 How to Download:  https://www.youtube.com/watch?v=fxu4w1ux3Eo&ab_channel=Showflix </b>\n\n" f"<b>📞 Join us : @showflix_movie , @showflix_group </b>\n\n",
        quote=True,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Join Our Group', url="https://telegram.me/showflix_group")]])
      
        
    )
