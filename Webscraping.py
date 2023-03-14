import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
import base64
import requests
import time
from streamlit_option_menu import option_menu
import io
from email.message import EmailMessage
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from twilio.rest import Client
import random
import warnings
warnings.filterwarnings('ignore')
import  streamlit_toggle as tog

username = st.secrets['username']
token = st.secrets['token']
account_sid = st.secrets['account_sid']
auth_token = st.secrets['auth_token']

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}
logo = 'https://raw.githubusercontent.com/PabloCaSan/Odillia/main/Odillia_Wordmark.jpg'

iconos = ['https://raw.githubusercontent.com/PabloCaSan/Odillia/main/iconos_01.png'
        ,'https://raw.githubusercontent.com/PabloCaSan/Odillia/main/iconos_02.png'
        ,'https://raw.githubusercontent.com/PabloCaSan/Odillia/main/iconos_03.png']

redes = ['https://raw.githubusercontent.com/PabloCaSan/Odillia/main/redes_01.png'
        ,'https://raw.githubusercontent.com/PabloCaSan/Odillia/main/redes_02.png'
        ,'https://raw.githubusercontent.com/PabloCaSan/Odillia/main/redes_03.png'
        ,'https://raw.githubusercontent.com/PabloCaSan/Odillia/main/redes_04.png']

ribbon = 'https://raw.githubusercontent.com/PabloCaSan/Odillia/main/aviso_ribbon.png'
icono_aviso = 'https://raw.githubusercontent.com/PabloCaSan/Odillia/main/icono-aviso.png'
aviso_fondo = 'https://raw.githubusercontent.com/PabloCaSan/Odillia/main/aviso_fondo.jpg'

client = Client(account_sid, auth_token) 

FakeSTI = None
FakeIL = None
FakeILWL = None

if 'carrito_de_compras' not in st.session_state:
    st.session_state['carrito_de_compras'] = []

if 'carrito_de_compras_df' not in st.session_state:
    st.session_state['carrito_de_compras_df'] = None

if 'page_change' not in st.session_state:
    st.session_state['page_change'] = 1

if 'STI' not in st.session_state:
	st.session_state['STI'] = None

if 'selected3' not in st.session_state:
    st.session_state['selected3'] = None

if 'IL' not in st.session_state:
	st.session_state['IL'] = None

if 'SKULink' not in st.session_state:
	st.session_state['SKULink'] = None

if 'SKULink2' not in st.session_state:
	st.session_state['SKULink2'] = None

if 'SKULinkRaw' not in st.session_state:
	st.session_state['SKULinkRaw'] = None

if 'Matrix' not in st.session_state:
	st.session_state['Matrix'] = None

if 'MatrixSegment' not in st.session_state:
	st.session_state['MatrixSegment'] = None

if 'MatrixCategory' not in st.session_state:
	st.session_state['MatrixCategory'] = None

if 'MatrixRaw' not in st.session_state:
	st.session_state['MatrixRaw'] = None

if 'Purchased_items_name_Raw' not in st.session_state:
    st.session_state['Purchased_items_name_Raw'] = None

if 'count1' not in st.session_state:
	st.session_state['count1'] = 1

if 'count2' not in st.session_state:
	st.session_state['count2'] = 1

if 'count3' not in st.session_state:
	st.session_state['count3'] = 1

if 'Description' not in st.session_state:
    st.session_state['Description'] = None

if 'Name' not in st.session_state:
    st.session_state['Name'] = None

if 'option2' not in st.session_state:
    st.session_state['option2'] = None

if 'SendCustomerRecommendations' not in st.session_state:
    st.session_state['SendCustomerRecommendations'] = None

if 'images_list' not in st.session_state:
    st.session_state['images_list'] = None

if 'captions_list' not in st.session_state:
    st.session_state['captions_list'] = None

if 'images_list2' not in st.session_state:
    st.session_state['images_list2'] = None

if 'captions_list2' not in st.session_state:
    st.session_state['captions_list2'] = None

if 'images_list3' not in st.session_state:
    st.session_state['images_list3'] = None

if 'captions_list3' not in st.session_state:
    st.session_state['captions_list3'] = None

if 'destinatario' not in st.session_state:
    st.session_state['destinatario'] = None

if 'numero' not in st.session_state:
    st.session_state['numero'] = None

if 'selectedSegment' not in st.session_state:
    st.session_state['selectedSegment'] = None

if 'selected2' not in st.session_state:
    st.session_state['selected2'] = None

if('show_more') not in st.session_state:
    st.session_state['show_more'] = 7

if('show_list') not in st.session_state:
    st.session_state['show_list'] = False

if('show_history') not in st.session_state:
    st.session_state['show_history'] = False

if('switch') not in st.session_state:
    st.session_state['switch'] = False

if('consejo') not in st.session_state:
    st.session_state['consejo'] = ""

if('promo') not in st.session_state:
    st.session_state['promo'] = ['2x1'
                                ,'50% de descuento'
                                ,'3x2'
                                ,'25% de descuento'
                                ,'5+1'
                                ,'20% de descuento'
                                ,'15% de descuento'
                                ,'10% de descuento']

def agregar_producto(add_item):
    st.session_state['carrito_de_compras'].append(add_item)

def quitar_producto(from_list, remove_item):
    del from_list[max([index for (index, item) in enumerate(from_list) if item==remove_item])]

def next_page():
    st.empty()
    st.session_state['page_change'] += 1

def final_page():
    if(st.session_state['selected3']=='Email'):
        if(st.session_state['selected2']=='Por cliente'):
            send_CustomerEmail(st.session_state['Name'],st.session_state['destinatario'],st.session_state['images_list'],st.session_state['captions_list'])
        if(st.session_state['selected2']=='Por producto'):
            send_ProductEmail(st.session_state['option2'],st.session_state['destinatario'],st.session_state['images_list2'],st.session_state['captions_list2'])

    if(st.session_state['selected3']=='SMS'):
        if(st.session_state['selected2']=='Por cliente'):
            send_SMS(st.session_state['Name'],st.session_state['numero'],st.session_state['captions_list'])
        if(st.session_state['selected2']=='Por producto'):
            send_SMS(st.session_state['option2'],st.session_state['numero'],st.session_state['captions_list2'])

    if(st.session_state['selected3']=='Whatsapp'):
        if(st.session_state['selected2']=='Por cliente'):
            send_CustomerWhatsapp(st.session_state['Name'],st.session_state['numero'],st.session_state['images_list'],st.session_state['captions_list'])
        if(st.session_state['selected2']=='Por producto'):
            send_ProductWhatsapp(st.session_state['option2'],st.session_state['numero'],st.session_state['images_list2'],st.session_state['captions_list2'])

    st.empty()
    st.session_state['page_change'] += 1

def previous_page():
    st.empty()
    st.session_state['page_change'] -= 1

def first_page():
    st.empty()
    st.session_state['page_change'] = 1

def show_more():
    st.session_state['show_more'] = 14

def show_less():
    st.session_state['show_more'] = 7

def show_list():
    st.session_state['show_list'] = True

def hide_list():
    st.session_state['show_list'] = False

def show_history():
    st.session_state['show_history'] = True

def hide_history():
    st.session_state['show_history'] = False

def hide_everything():
    show_less()
    hide_list()
    hide_history()    

def send_SMS(name, number, captions):
    message = client.messages.create(  
                              messaging_service_sid='MG4932b4f54d41cd28ff0f0d0bca2a314e', 
                              body='''Porque te interesó ''' + name + ''' Odillia te recomienda
                              
                              ''' 
                              + captions[0] + '''
                              
                              '''
                              + captions[1] + '''
                              
                              '''
                              + captions[2] + '''
                              
                              '''
                              + captions[3] + '''
                              
                              '''
                              + captions[4] + '''
                              
                              '''
                              + captions[5] + '''
                              
                              '''
                              + captions[6] + '''
                              
                              ''',      
                              to='+52' + number, 
                          ) 

def send_ProductWhatsapp(product, number, images, captions):
    if(len(captions) <= 7):
        message = client.messages.create( 
                                    from_='whatsapp:+14155238886',  
                                    body='*Porque te interesó _' + product + '_*',      
                                    to='whatsapp:+521'+ number,
                                ) 
        time.sleep(3)
        for i in range(len(images)):
            message = client.messages.create( 
                                    from_='whatsapp:+14155238886',  
                                    body=captions[i],      
                                    media_url=images[i],
                                    to='whatsapp:+521'+ number,
                                ) 
            time.sleep(1)
    else:
        message = client.messages.create( 
                                    from_='whatsapp:+14155238886',  
                                    body='*Porque te interesó _' + product + '_*',      
                                    to='whatsapp:+521'+ number,
                                ) 
        time.sleep(3)
        for i in range(0,7):
            message = client.messages.create( 
                                    from_='whatsapp:+14155238886',  
                                    body=captions[i],      
                                    media_url=images[i],
                                    to='whatsapp:+521'+ number,
                                ) 
            time.sleep(1)

def send_CustomerWhatsapp(name, number, images, captions):
    if(len(captions) <= 7):
        message = client.messages.create( 
                                    from_='whatsapp:+14155238886',  
                                    body='*Hola _' + name + '_, Odillia tiene las mejores recomendaciones para ti*',      
                                    to='whatsapp:+521'+ number,
        )
        time.sleep(3)                        
        for i in range(len(images)):
            message = client.messages.create( 
                                    from_='whatsapp:+14155238886',  
                                    body=captions[i],      
                                    media_url=images[i],
                                    to='whatsapp:+521'+ number,
            )
            time.sleep(1)    
    else:
        message = client.messages.create( 
                                    from_='whatsapp:+14155238886',  
                                    body='*Hola _' + name + '_, Odillia tiene las mejores recomendaciones para ti*',      
                                    to='whatsapp:+521'+ number, 
                                ) 
        time.sleep(3)                        
        for i in range(0,7):
            message = client.messages.create( 
                                    from_='whatsapp:+14155238886',  
                                    body=captions[i],      
                                    media_url=images[i],
                                    to='whatsapp:+521'+ number, 
                                ) 
            time.sleep(1)    

def send_ProductEmail(product, receiver, images, captions):
    email = EmailMessage()
    email["From"] = "odillia.ssis@gmail.com"
    email["To"] = receiver
    email["Subject"] = "¡Odillia tiene las mejores recomendaciones solo para ti!"
    email.set_content("¡Hola!")
    email.add_alternative(short_html_CodeBlock(product
                                            ,captions
                                            ,images
                                            ,"Porque te interesó "), subtype="html")
    smtp = smtplib.SMTP("smtp.gmail.com", port=587)
    smtp.starttls()
    smtp.login(email['From'], "retslknvxvcwxxjn")
    smtp.send_message(email)
    smtp.quit()

def send_CustomerEmail(name, receiver, images, captions):
    email = EmailMessage()
    email["From"] = "odillia.ssis@gmail.com"
    email["To"] = receiver
    email["Subject"] = "¡Odillia tiene las mejores recomendaciones solo para ti!"
    email.set_content("¡Hola!")
    email.add_alternative(short_html_CodeBlock(name
                                            ,captions
                                            ,images
                                            ,"Hola "
                                            ,st.session_state['consejo'][random.randint(0,2)]
                                            ,st.session_state['promo'][random.randint(0,7)]
                                            ,st.session_state['promo'][random.randint(0,7)]
                                            ,st.session_state['promo'][random.randint(0,7)]
                                            ,st.session_state['promo'][random.randint(0,7)]
                                            ,st.session_state['promo'][random.randint(0,7)]
                                            ,st.session_state['promo'][random.randint(0,7)]
                                            ,st.session_state['promo'][random.randint(0,7)]), subtype="html")
    smtp = smtplib.SMTP("smtp.gmail.com", port=587)
    smtp.starttls()
    smtp.login(email['From'], "retslknvxvcwxxjn")
    smtp.sendmail(email['From'], receiver, email.as_string())
    smtp.quit()

def funnel_html(category1,percentage1,category2,percentage2,category3,percentage3,category4,percentage4,category5,percentage5):
    html_code = ''' 
                <style>

                .item {
                position: relative;
                }

                .item label {
                position: absolute;
                text-shadow: 0px 0.6px 1px #000;
                top: -20px;
                }
                .item1 {
                    margin: 0 140px;
                    border-left: 20px solid transparent;
                    border-right: 20px solid transparent;
                    border-top: 50px solid #41559F;
                    border-radius: 10px;
                }
                .item2 {
                    margin: 0 160px;
                    border-left: 20px solid transparent;
                    border-right: 20px solid transparent;
                    border-top: 50px solid #5167B8;
                    border-radius: 10px;
                }
                .item3 {
                    margin: 0 180px;
                    border-left: 20px solid transparent;
                    border-right: 20px solid transparent;
                    border-top: 50px solid #6E81C4;
                    border-radius: 10px;
                }
                .item4 {
                    margin: 0 200px;
                    border-left: 20px solid transparent;
                    border-right: 20px solid transparent;
                    border-top: 50px solid #8B9AD0;
                    border-radius: 10px;
                }
                .item5 {
                    margin: 0 220px;
                    border-left: 20px solid transparent;
                    border-right: 20px solid transparent;
                    border-top: 50px solid #7CA2DE;
                    border-radius: 10px;
                }
                .div_label_lft{
                    text-align: left;
                }
                .div_label_rgt{
                    text-align: right;
                }
                .lft{
                    color: #fff;
                    margin-left: -7px;
                    margin-top: -15px;
                }
                .rgt{
                    color: #fff;
                    margin-left: -35px;
                    margin-top: -15px;
                }

                .top5{
                    text-align: left;
                    font-size: 25px;
                }

                </style>

                <html>
                    <h1 class='top5'> Top 5 categorías compradas </h1>
                    <div class="item item1" title="1">
                        <div class='div_label_lft'>
                            <label class='lft'>''' + category1 + '''</label>
                        </div>
                        <div class='div_label_rgt'>
                            <label class='rgt'>''' + percentage1 + '''%</label>
                        </div>
                    </div>
                    <div class="item item2" title="2">
                        <div class='div_label_lft'>
                            <label class='lft'>''' + category2 + '''</label>
                        </div>
                        <div class='div_label_rgt'>
                            <label class='rgt'>''' + percentage2 + '''%</label>
                        </div>
                    </div>
                    <div class="item item3" title="3">
                        <div class='div_label_lft'>
                            <label class='lft'>''' + category3 + '''</label>
                        </div>
                        <div class='div_label_rgt'>
                            <label class='rgt'>''' + percentage3 + '''%</label>
                        </div>
                    </div>
                    <div class="item item4" title="4">
                        <div class='div_label_lft'>
                            <label class='lft'>''' + category4 + '''</label>
                        </div>
                        <div class='div_label_rgt'>
                            <label class='rgt'>''' + percentage4 + '''%</label>
                        </div>
                    </div>
                    <div class="item item5" title="5">
                        <div class='div_label_lft'>
                            <label class='lft'>''' + category5 + '''</label>
                        </div>
                        <div class='div_label_rgt'>
                            <label class='rgt'>''' + percentage5 + '''%</label>
                        </div>
                    </div>
                </html>
                '''
    return html_code

def html_CodeBlock(item, captions, images, message1, message2, promo1, promo2, promo3, promo4, promo5, promo6, promo7):
    html_code = '''
                <!doctype html>
                <html>
                <head>
                <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
                <link href="https://fonts.googleapis.com/css2?family=Albert+Sans:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap" rel="stylesheet">
                <style type="text/css">
                @charset "UTF-8";
                    
                img, video, object {
                    max-width: 100%;
                    max-height: 200px;
                    height: auto;
                    width: auto\9; /* ie8 */
                }

                body {
                    background-color: #FFF;
                    margin: 0px;
                }

                div {
                    width: 100%;
                    display: inline-flex;
                }    
                .base {
                    width: 834px;
                    height: 2097px;
                    margin-left: auto;
                    margin-right: auto;
                    margin-top: 25px;
                    margin-bottom: 50px;
                    background-color: #E1E1E1;
                    padding-top: 20px;
                    padding-left: 20px;
                    padding-right: 20px;
                }
                    
                .logotipo{
                    width: 834px;
                    height: 172px;
                    background-color: #ededed;
                    float: left;
                }

                .info1{
                    width: 834px;
                    height: 200px;
                    background-color: #ededed;
                    font-family: 'Albert Sans', sans-serif;
                    color: #7c7c7c;
                    font-size: 23px;
                    font-weight: 400;
                    text-align: center;
                    float: left;
                    margin-bottom: 20px;
                    border-radius: 20px;
                }

                .advice {
                    color: #00A676;
                    font-weight: 600;
                }
                
                .info{
                    width: 834px;
                    height: 200px;
                    background-color: #ededed;
                    font-family: 'Albert Sans', sans-serif;
                    color: #7c7c7c;
                    font-size: 23px;
                    font-weight: 400;
                    text-align: center;
                    float: left;
                    margin-bottom: 20px;
                }

                .producto_a {
                    width: 407px;
                    height: 400px;
                    float: left;
                    margin-bottom: 20px;
                    background-color: #fff;
                    text-align: center;
                    align-self: flex-end;
                }
                
                .producto_a1 {
                    width: 407px;
                    height: 400px;
                    float: left;
                    margin-bottom: 20px;
                    background-color: #fff;
                    text-align: center;
                    align-self: flex-end;
                }

                .producto_c {
                    width: 265px;
                    height: 400px;
                    float: left;
                    margin-bottom: 20px;
                    background-color: #fff;
                    text-align: center;
                    align-self: flex-end;
                }

                .icons {
                    width: 834px;
                    height: 186px;
                    background-color: #ededed;
                    text-align: center;
                    float: left;
                    border-top-left-radius: 20px;
                    border-top-right-radius: 20px;
                }

                .icon {
                    width: 33.33%;
                    height: auto;
                    float: left;
                }
                    .redes{
                        width: 834px;
                        height: 95px;
                        background-color: #ededed;
                        text-align: center;
                        float: left;
                        border-bottom-left-radius: 20px;
                        border-bottom-right-radius: 20px;
                        margin-bottom: 20px;
                    }
                    h1 {
                    font-family: 'Albert Sans', sans-serif;
                    color: #7c7c7c;
                    font-size: 36px;
                }
                    .unsuscribe {
                        font-size: 15px;
                        margin-top: 80px;
                    }
                    
                    .pipe1{
                        font-family: 'Albert Sans', sans-serif;
                        color: #b72a4a;
                        font-size:10px;
                        color: #414243;
                        font-weight: bold;
                        line-height: 10px;
                    }
                    .pipe2{
                        font-family: 'Albert Sans', sans-serif;
                        color: #b72a4a;
                        font-size:18px;
                        color: #8E94F2;
                        font-weight: bold;
                        line-height: 10px;
                    }
                    .pipe3{
                        font-family: 'Albert Sans', sans-serif;
                        color: #b72a4a;
                        font-size:14px;
                        color: #414243;
                        font-weight: 400;
                        line-height: 0px;
                    }
                    input.btn {
                    width: 225px;
                    height: 40px;
                    background-color: #354c82;
                    border-radius: 10px;
                    font-family: 'Albert Sans', sans-serif;
                    font-size: 16px;
                    font-weight: 600;
                    color: #FFFFFF;
                    cursor: pointer;
                    border-width: 0px;
                    border-style: none;
                    text-align: center;
                
                }

                input.btn:hover {
                    background: #2271da;
                    font-weight: 600;
                }
                    .frase {
                        width: 100%;
                        text-align: center;
                        font-family: 'Albert Sans', sans-serif;
                    font-size: 13px;
                        color: #414243;
                        margin-top: 25px;
                    }
                    a.liga{
                    font-weight: 600;
                    color: #414243;
                    text-decoration: none;		
                    }
                    
                    a.liga:hover{
                    font-weight: 600;
                    color: #b72a4a;
                    text-decoration: none;		
                    }
                    a.liga2{
                    font-weight: 600;
                    color: #414243;
                    text-decoration: none;		
                    }
                    
                    a.liga2:hover{
                    font-weight: 600;
                    color: #b72a4a;
                    text-decoration: none;		
                    }
                    
                    .aviso_base {
                    width: 835px;
                    height: 346px;
                    float: left;
                    margin-bottom: 20px;
                    background-image: url('''+ aviso_fondo +''');
                    text-align: right;
                    background-repeat: no-repeat;
                    }
                    
                    .aviso_ribbon {
                    width: 835px;
                    height: auto;
                    float: left;
                    z-index: 2;
                    position: absolute;
                    text-align: left;
                    }
                    
                    .aviso_name {
                    width: 640px;
                    height: auto;
                    padding-right: 160px;
                    padding-left: 35px;
                    padding-top: 10px;
                    float: left;
                    z-index: 1;
                    position: absolute;
                    font-family: 'Roboto', sans-serif;
                    color: #ffffff;
                    font-size: 46px;
                    text-align: right;
                    line-height: 20px;
                    font-weight: 400;
                    }
                    
                    .aviso_mensaje {
                    width: 600px;
                    height: auto;
                    padding-right: 200px;
                    padding-left: 35px;
                    padding-top:  167px; 
                    float: left;
                    z-index: 1;
                    position: absolute;
                    font-family: 'Roboto', sans-serif;
                    color: #3368AA;
                    text-align: right;
                    font-size: 28px;
                    line-height: 32px;
                    }
                    
                    .aviso_frase {
                    font-weight: bold;
                    font-size: 32px;
                    line-height: 0px;
                    }
                    
                    .aviso_name_txt {
                    font-size: 80px;
                    line-height: 0px;
                    }

                @media screen{
                    
                    .base {
                        width: 95.42%;
                        height: auto;
                        padding-right: 2.28%;
                        padding-left: 2.28%;
                        float: left;
                        border-radius: 20px;
                    }
                    
                    .logotipo{
                        width: 100%;
                        height: auto;
                    }

                    .info1{
                        width: 100%;
                        height: 200px;
                        background-color: #ededed;
                        font-family: 'Albert Sans', sans-serif;
                        color: #7c7c7c;
                        font-size: 23px;
                        font-weight: 400;
                        text-align: center;
                        float: left;
                        margin-bottom: 20px;
                        border-radius: 20px;
                    }

                    .advice {
                        color: #00A676;
                        font-weight: 600;
                    }

                    .info{
                        width: 100%;
                        height: 200px;
                        background-color: #ededed;
                        font-family: 'Albert Sans', sans-serif;
                        color: #7c7c7c;
                        font-size: 23px;
                        font-weight: 400;
                        text-align: center;
                        float: left;
                        margin-bottom: 20px;
                    }

                    .producto_a {
                        width: 48.80%;
                        height: auto;
                        margin-right: 1%;
                        padding-bottom: 20px;
                        border-radius: 20px;
                        align-self: flex-end;
                    }

                    .producto_a1 {
                        width: 48.80%;
                        height: auto;
                        margin-left: 1%;
                        padding-bottom: 20px;
                        border-radius: 20px;
                        align-self: flex-end;
                    }

                    .producto_c {
                        width: 100%;
                        height: auto;
                        padding-bottom: 20px;
                        border-radius: 20px;
                        align-self: flex-end;
                    }
                    
                    .redes{
                        width: 100%;
                        height: auto;
                        border-bottom-left-radius: 20px;
                        border-bottom-right-radius: 20px;
                        margin-bottom: 20px;
                    }
                    
                    .icons{
                        width: 100%;
                        height: auto;
                        border-top-left-radius: 20px;
                        border-top-right-radius: 20px;
                    }

                    .aviso_base {
                    width: 99.90%;
                    }
                    
                    .aviso_ribbon {
                    width: 95.50%;
                    }
                    
                    .aviso_name {
                    width: 73.22%;
                    padding-right: 18.30%;
                    padding-left: 4%;
                    }
                    
                    .aviso_mensaje {
                    width: 68.64%;
                    padding-right: 22.88%;
                    padding-left: 4%;
                    }
                       
                }
                    
                    @media screen and (max-width: 768px) {
                        
                        .producto_c {
                            width: 100%;
                            margin-right: 0%;
                            align-self: flex-end;
                        }

                        input.btn {
                            width: 85%;
                            font-size: 13px;
                        }

                        .pipe1{
                            font-size:10px;
                            line-height: 10px;
                        }

                        .pipe2{
                            color: #8E94F2;
                            font-size:18px;
                            line-height: 10px;
                        }

                        .pipe3{
                            font-size:12px;
                            color: #414243;
                        }

                        	.aviso_name {
                                font-size: 48px;
                                line-height: 10px;
                                        width: 73.22%;
                                padding-right: 18.30%;
                                padding-left: 4%;
                                }
                                
                                .aviso_mensaje {
                                font-size: 22px;
                                line-height: 20px;
                                padding-top:  147px;
                                    width: 68.64%;
                                padding-right: 22.88%;
                                padding-left: 4%;
                                }
                                    
                                    .aviso_frase {
                                font-weight: bold;
                                font-size: 25px;
                                line-height: 25px;
                                }
                                
                                .aviso_name_txt {
                                font-size: 60px;
                                line-height: 0px;
                                }
                        
                    }

                    @media screen and (max-width: 630px) {
                        .aviso_name {
                    font-size: 46px;
                    line-height: 10px;
                            width: 67.22%;
                    padding-right: 24.30%;
                    padding-left: 4%;
                    }
                    
                    .aviso_mensaje {
                    font-size: 20px;
                    line-height: 20px;
                    padding-top:  147px;
                        width: 57.64%;
                    padding-right: 33.88%;
                    padding-left: 4%;
                    }
                    }

                </style>
                <meta charset="UTF-8">
                <title>Odillia</title>
                </head>

                <body>
                    <section class="base">
                        <section class="aviso_base">
                            <section class="aviso_ribbon"><img src="''' + ribbon + '''" alt="" width="213" height="77"/></section>
                            <section class="aviso_name"><p>'''+ message1 +'''</p><span class="aviso_name_txt">'''+ item +'''!</span></section>
                        <section class="aviso_mensaje"><p class="aviso_frase">'''+ message2 +'''</p> 
                        <p>Nuestros suplementos te ayudan a alcanzar tus metas de salud y bienestar.</p></section>
                            <img src="''' + icono_aviso + '''" alt=""/></section>
                        
                        <div class="div_1">
                            <section class="producto_c">
                            <p class="pipe2">''' + promo1 + '''</p>
                            <img src="''' + images[0] + '''" width="204" height="204" alt="Odillia"/>
                            <p class="pipe1">''' + captions[0] + '''</p>
                            <input type="button" name="button" id="button" value="COMPRA AHORA" class="btn">
                            </section>
                        </div>

                        <div class="div_2">
                            <section class="producto_a">
                            <p class="pipe2">''' + promo2 + '''</p>
                            <img src="''' + images[1] + '''" width="204" height="204" alt="Odillia"/>
                            <p class="pipe1">''' + captions[1] + '''</p>
                            <input type="button" name="button" id="button" value="COMPRA AHORA" class="btn">
                            </section>
                        
                            <section class="producto_a1">
                            <p class="pipe2">''' + promo3 + '''</p>
                            <img src="''' + images[2] + '''" width="204" height="204" alt="Odillia"/>
                            <p class="pipe1">''' + captions[2] + '''</p>
                            <input type="button" name="button" id="button" value="COMPRA AHORA" class="btn">
                            </section>
                        </div>
                            
                        <div class="div_2">
                            <section class="producto_a">
                            <p class="pipe2">''' + promo4 + '''</p>
                            <img src="''' + images[3] + '''" width="204" height="204" alt="Odillia"/>
                            <p class="pipe1">''' + captions[3] + '''</p>
                            <input type="button" name="button" id="button" value="COMPRA AHORA" class="btn">
                            </section>
                        
                            <section class="producto_a1">
                            <p class="pipe2">''' + promo5 + '''</p>
                            <img src="''' + images[4] + '''" width="204" height="204" alt="Odillia"/>
                            <p class="pipe1">''' + captions[4] + '''</p>
                            <input type="button" name="button" id="button" value="COMPRA AHORA" class="btn">
                            </section>
                        </div>

                        <div class="div_2">
                            <section class="producto_a">
                            <p class="pipe2">''' + promo6 + '''</p>
                            <img src="''' + images[5] + '''" width="204" height="204" alt="Odillia"/>
                            <p class="pipe1">''' + captions[5] + '''</p>
                            <input type="button" name="button" id="button" value="COMPRA AHORA" class="btn">
                            </section>
                            
                            <section class="producto_a1">
                            <p class="pipe2">''' + promo7 + '''</p>
                            <img src="''' + images[6] + '''" width="204" height="204" alt="Odillia"/>
                            <p class="pipe1">''' + captions[6] + '''</p>
                            <input type="button" name="button" id="button" value="COMPRA AHORA" class="btn">
                            </section>
                        </div>

                        <section class="icons">
                            <div  class="icon">
                                <img src="''' + iconos[0] + '''" width="278" height="186" alt="Odillia"/>
                            </div>
                            <div class="icon">
                                <img src="''' + iconos[1] + '''" width="277" height="186" alt="Odillia"/>
                            </div>
                            <div class="icon">
                                <img src="''' + iconos[2] + '''" width="279" height="186" alt="Odillia"/>
                            </div>
                            </section>
                        <section class="redes">
                            <img src="''' + redes[0] + '''" width="71" height="95" alt="Odillia"/>
                            <img src="''' + redes[1] + '''" width="71" height="95" alt="Odillia"/>
                            <img src="''' + redes[2] + '''" width="71" height="95" alt="Odillia"/>
                            <img src="''' + redes[3] + '''" width="69" height="95" alt="Odillia"/>
                        </section>
                    </section>
                </body>
                </html>'''
    return html_code

def html_CodeBlock_14(item, captions, images, message1, message2, promo1, promo2, promo3, promo4, promo5, promo6, promo7, promo8, promo9, promo10, promo11, promo12, promo13, promo14):
    html_code = '''
                <!doctype html>
                <html>
                <head>
                <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
                <link href="https://fonts.googleapis.com/css2?family=Albert+Sans:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap" rel="stylesheet">
                <style type="text/css">
                @charset "UTF-8";
                    
                img, video, object {
                    max-width: 100%;
                    max-height: 200px;
                    height: auto;
                    width: auto\9; /* ie8 */
                }

                body {
                    background-color: #FFF;
                    margin: 0px;
                }

                div {
                    width: 100%;
                    display: inline-flex;
                }    
                .base {
                    width: 834px;
                    height: 2097px;
                    margin-left: auto;
                    margin-right: auto;
                    margin-top: 25px;
                    margin-bottom: 50px;
                    background-color: #E1E1E1;
                    padding-top: 20px;
                    padding-left: 20px;
                    padding-right: 20px;
                }
                    
                .logotipo{
                    width: 834px;
                    height: 172px;
                    background-color: #ededed;
                    float: left;
                }

                .info1{
                    width: 834px;
                    height: 200px;
                    background-color: #ededed;
                    font-family: 'Albert Sans', sans-serif;
                    color: #7c7c7c;
                    font-size: 23px;
                    font-weight: 400;
                    text-align: center;
                    float: left;
                    margin-bottom: 20px;
                    border-radius: 20px;
                }

                .advice {
                    color: #00A676;
                    font-weight: 600;
                }
                
                .info{
                    width: 834px;
                    height: 200px;
                    background-color: #ededed;
                    font-family: 'Albert Sans', sans-serif;
                    color: #7c7c7c;
                    font-size: 23px;
                    font-weight: 400;
                    text-align: center;
                    float: left;
                    margin-bottom: 20px;
                }

                .producto_a {
                    width: 407px;
                    height: 400px;
                    float: left;
                    margin-bottom: 20px;
                    background-color: #fff;
                    text-align: center;
                    align-self: flex-end;
                }
                
                .producto_a1 {
                    width: 407px;
                    height: 400px;
                    float: left;
                    margin-bottom: 20px;
                    background-color: #fff;
                    text-align: center;
                    align-self: flex-end;
                }

                .producto_c {
                    width: 265px;
                    height: 400px;
                    float: left;
                    margin-bottom: 20px;
                    background-color: #fff;
                    text-align: center;
                    align-self: flex-end;
                }

                .icons {
                    width: 834px;
                    height: 186px;
                    background-color: #ededed;
                    text-align: center;
                    float: left;
                    border-top-left-radius: 20px;
                    border-top-right-radius: 20px;
                }

                .icon {
                    width: 33.33%;
                    height: auto;
                    float: left;
                }
                    .redes{
                        width: 834px;
                        height: 95px;
                        background-color: #ededed;
                        text-align: center;
                        float: left;
                        border-bottom-left-radius: 20px;
                        border-bottom-right-radius: 20px;
                        margin-bottom: 20px;
                    }
                    h1 {
                    font-family: 'Albert Sans', sans-serif;
                    color: #7c7c7c;
                    font-size: 36px;
                }
                    .unsuscribe {
                        font-size: 15px;
                        margin-top: 80px;
                    }
                    
                    .pipe1{
                        font-family: 'Albert Sans', sans-serif;
                        color: #b72a4a;
                        font-size:10px;
                        color: #414243;
                        font-weight: bold;
                        line-height: 10px;
                    }
                    .pipe2{
                        font-family: 'Albert Sans', sans-serif;
                        color: #8E94F2;
                        font-size:18px;
                        color: #354c82;
                        font-weight: bold;
                        line-height: 10px;
                    }
                    .pipe3{
                        font-family: 'Albert Sans', sans-serif;
                        color: #b72a4a;
                        font-size:14px;
                        color: #414243;
                        font-weight: 400;
                        line-height: 0px;
                    }
                    input.btn {
                    width: 225px;
                    height: 40px;
                    background-color: #354c82;
                    border-radius: 10px;
                    font-family: 'Albert Sans', sans-serif;
                    font-size: 16px;
                    font-weight: 600;
                    color: #FFFFFF;
                    cursor: pointer;
                    border-width: 0px;
                    border-style: none;
                    text-align: center;
                
                }

                input.btn:hover {
                    background: #2271da;
                    font-weight: 600;
                }
                    .frase {
                        width: 100%;
                        text-align: center;
                        font-family: 'Albert Sans', sans-serif;
                    font-size: 13px;
                        color: #414243;
                        margin-top: 25px;
                    }
                    a.liga{
                    font-weight: 600;
                    color: #414243;
                    text-decoration: none;		
                    }
                    
                    a.liga:hover{
                    font-weight: 600;
                    color: #b72a4a;
                    text-decoration: none;		
                    }
                    a.liga2{
                    font-weight: 600;
                    color: #414243;
                    text-decoration: none;		
                    }
                    
                    a.liga2:hover{
                    font-weight: 600;
                    color: #b72a4a;
                    text-decoration: none;		
                    }
                    
                @media screen{
                    
                    .base {
                        width: 95.42%;
                        height: auto;
                        padding-right: 2.28%;
                        padding-left: 2.28%;
                        float: left;
                        border-radius: 20px;
                    }
                    
                    .logotipo{
                        width: 100%;
                        height: auto;
                    }

                    .info1{
                        width: 100%;
                        height: 200px;
                        background-color: #ededed;
                        font-family: 'Albert Sans', sans-serif;
                        color: #7c7c7c;
                        font-size: 23px;
                        font-weight: 400;
                        text-align: center;
                        float: left;
                        margin-bottom: 20px;
                        border-radius: 20px;
                    }

                    .advice {
                        color: #00A676;
                        font-weight: 600;
                    }

                    .info{
                        width: 100%;
                        height: 200px;
                        background-color: #ededed;
                        font-family: 'Albert Sans', sans-serif;
                        color: #7c7c7c;
                        font-size: 23px;
                        font-weight: 400;
                        text-align: center;
                        float: left;
                        margin-bottom: 20px;
                    }

                    .producto_a {
                        width: 48.80%;
                        height: auto;
                        margin-right: 1%;
                        padding-bottom: 20px;
                        border-radius: 20px;
                        align-self: flex-end;
                    }

                    .producto_a1 {
                        width: 48.80%;
                        height: auto;
                        margin-left: 1%;
                        padding-bottom: 20px;
                        border-radius: 20px;
                        align-self: flex-end;
                    }

                    .producto_c {
                        width: 100%;
                        height: auto;
                        padding-bottom: 20px;
                        border-radius: 20px;
                        align-self: flex-end;
                    }
                    
                    .redes{
                        width: 100%;
                        height: auto;
                        border-bottom-left-radius: 20px;
                        border-bottom-right-radius: 20px;
                        margin-bottom: 20px;
                    }
                    
                    .icons{
                        width: 100%;
                        height: auto;
                        border-top-left-radius: 20px;
                        border-top-right-radius: 20px;
                    }
                    
                }
                    
                    @media screen and (max-width: 768px) {
                        
                        .producto_c {
                            width: 100%;
                            margin-right: 0%;
                            align-self: flex-end;
                        }

                        input.btn {
                            width: 85%;
                            font-size: 13px;
                        }

                        .pipe1{
                            font-size:10px;
                            line-height: 10px;
                        }

                        .pipe2{
                            color: #8E94F2;
                            font-size:18px;
                            line-height: 10px;
                        }

                        .pipe3{
                            font-size:12px;
                            color: #414243;
                        }
                        
                    }
                </style>
                <meta charset="UTF-8">
                <title>Odillia</title>
                </head>

                <body>
                    <section class="base">
                        <section class="info1"><h1>''' + message1 + item + '''</h1>
                        <p class="advice">''' + message2 + ''' </p>
                        </section>
                        
                        <div class="div_2">
                            <section class="producto_a">
                            <p class="pipe2">''' + promo1 + '''</p>
                            <img src="''' + images[0] + '''" width="204" height="204" alt="Odillia"/>
                            <p class="pipe1">''' + captions[0] + '''</p>
                            <input type="button" name="button" id="button" value="COMPRA AHORA" class="btn">
                            </section>
                        
                            <section class="producto_a1">
                            <p class="pipe2">''' + promo2 + '''</p>
                            <img src="''' + images[1] + '''" width="204" height="204" alt="Odillia"/>
                            <p class="pipe1">''' + captions[1] + '''</p>
                            <input type="button" name="button" id="button" value="COMPRA AHORA" class="btn">
                            </section>
                        </div>
                            
                        <div class="div_2">
                            <section class="producto_a">
                            <p class="pipe2">''' + promo3 + '''</p>
                            <img src="''' + images[2] + '''" width="204" height="204" alt="Odillia"/>
                            <p class="pipe1">''' + captions[2] + '''</p>
                            <input type="button" name="button" id="button" value="COMPRA AHORA" class="btn">
                            </section>
                        
                            <section class="producto_a1">
                            <p class="pipe2">''' + promo4 + '''</p>
                            <img src="''' + images[3] + '''" width="204" height="204" alt="Odillia"/>
                            <p class="pipe1">''' + captions[3] + '''</p>
                            <input type="button" name="button" id="button" value="COMPRA AHORA" class="btn">
                            </section>
                        </div>

                        <div class="div_2">
                            <section class="producto_a">
                            <p class="pipe2">''' + promo5 + '''</p>
                            <img src="''' + images[4] + '''" width="204" height="204" alt="Odillia"/>
                            <p class="pipe1">''' + captions[4] + '''</p>
                            <input type="button" name="button" id="button" value="COMPRA AHORA" class="btn">
                            </section>
                            
                            <section class="producto_a1">
                            <p class="pipe2">''' + promo6 + '''</p>
                            <img src="''' + images[5] + '''" width="204" height="204" alt="Odillia"/>
                            <p class="pipe1">''' + captions[5] + '''</p>
                            <input type="button" name="button" id="button" value="COMPRA AHORA" class="btn">
                            </section>
                        </div>

                        <div class="div_2">
                            <section class="producto_a">
                            <p class="pipe2">''' + promo7 + '''</p>
                            <img src="''' + images[6] + '''" width="204" height="204" alt="Odillia"/>
                            <p class="pipe1">''' + captions[6] + '''</p>
                            <input type="button" name="button" id="button" value="COMPRA AHORA" class="btn">
                            </section>
                            
                            <section class="producto_a1">
                            <p class="pipe2">''' + promo8 + '''</p>
                            <img src="''' + images[7] + '''" width="204" height="204" alt="Odillia"/>
                            <p class="pipe1">''' + captions[7] + '''</p>
                            <input type="button" name="button" id="button" value="COMPRA AHORA" class="btn">
                            </section>
                        </div>

                        <div class="div_2">
                            <section class="producto_a">
                            <p class="pipe2">''' + promo9 + '''</p>
                            <img src="''' + images[8] + '''" width="204" height="204" alt="Odillia"/>
                            <p class="pipe1">''' + captions[8] + '''</p>
                            <input type="button" name="button" id="button" value="COMPRA AHORA" class="btn">
                            </section>
                            
                            <section class="producto_a1">
                            <p class="pipe2">''' + promo10 + '''</p>
                            <img src="''' + images[9] + '''" width="204" height="204" alt="Odillia"/>
                            <p class="pipe1">''' + captions[9] + '''</p>
                            <input type="button" name="button" id="button" value="COMPRA AHORA" class="btn">
                            </section>
                        </div>

                        <div class="div_2">
                            <section class="producto_a">
                            <p class="pipe2">''' + promo11 + '''</p>
                            <img src="''' + images[10] + '''" width="204" height="204" alt="Odillia"/>
                            <p class="pipe1">''' + captions[10] + '''</p>
                            <input type="button" name="button" id="button" value="COMPRA AHORA" class="btn">
                            </section>
                            
                            <section class="producto_a1">
                            <p class="pipe2">''' + promo12 + '''</p>
                            <img src="''' + images[11] + '''" width="204" height="204" alt="Odillia"/>
                            <p class="pipe1">''' + captions[11] + '''</p>
                            <input type="button" name="button" id="button" value="COMPRA AHORA" class="btn">
                            </section>
                        </div>

                        <div class="div_2">
                            <section class="producto_a">
                            <p class="pipe2">''' + promo13 + '''</p>
                            <img src="''' + images[12] + '''" width="204" height="204" alt="Odillia"/>
                            <p class="pipe1">''' + captions[12] + '''</p>
                            <input type="button" name="button" id="button" value="COMPRA AHORA" class="btn">
                            </section>
                            
                            <section class="producto_a1">
                            <p class="pipe2">''' + promo14 + '''</p>
                            <img src="''' + images[13] + '''" width="204" height="204" alt="Odillia"/>
                            <p class="pipe1">''' + captions[13] + '''</p>
                            <input type="button" name="button" id="button" value="COMPRA AHORA" class="btn">
                            </section>
                        </div>

                        <section class="icons">
                            <div  class="icon">
                                <img src="''' + iconos[0] + '''" width="278" height="186" alt="Odillia"/>
                            </div>
                            <div class="icon">
                                <img src="''' + iconos[1] + '''" width="277" height="186" alt="Odillia"/>
                            </div>
                            <div class="icon">
                                <img src="''' + iconos[2] + '''" width="279" height="186" alt="Odillia"/>
                            </div>
                            </section>
                        <section class="redes">
                            <img src="''' + redes[0] + '''" width="71" height="95" alt="Odillia"/>
                            <img src="''' + redes[1] + '''" width="71" height="95" alt="Odillia"/>
                            <img src="''' + redes[2] + '''" width="71" height="95" alt="Odillia"/>
                            <img src="''' + redes[3] + '''" width="69" height="95" alt="Odillia"/>
                        </section>
                    </section>
                </body>
                </html>'''
    return html_code

def short_html_CodeBlock(item, captions, images, message1, message2, promo1, promo2, promo3, promo4, promo5, promo6, promo7):
    html_code = '''
                <!doctype html>
                <html>
                <head>
                <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
                <link href="https://fonts.googleapis.com/css2?family=Albert+Sans:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap" rel="stylesheet">
                <meta charset="UTF-8">
                <title>Odillia</title>
                </head>
                
                <header>
                <section class="logotipo" style="width: 100%; height: auto; float: left;">
                <img src="'''+ logo + '''" width="50%" height="auto" alt="" style="border-radius: 20px; align-self: end;"/>
                </section>
                </header>
                <body style="background-color: #FFF; margin: 0px;">
                    <section class="base" style="margin-left: auto; margin-right: auto; margin-top: 25px; margin-bottom: 50px; background-color: #E1E1E1; padding-top: 20px; padding-left: 20px; padding-right: 20px; width: 95.42%; height: auto; padding-right: 2.28%; padding-left: 2.28%; float: left; border-radius: 20px;">
                        <section class="info1" style="width: 100%; height: 200px; background-color: #ededed; font-family: 'Albert Sans', sans-serif; color: #7c7c7c; font-size: 23px; font-weight: 400; text-align: center; float: left; margin-bottom: 20px; border-radius: 20px;">
                            <h1 style="font-family: 'Albert Sans', sans-serif; color: #7c7c7c; font-size: 36px;">&#161;''' + message1 + item + '''&#33;</br></h1>
                            <p class="advice" style="color: #00A676;">''' + message2 + ''' </p>
                        </section>
                        
                        <div class="div_1" style="width: 100%; display: inline-flex;">
                            <section class="producto_c" style="width: 100%; margin-right: 0%; align-self: flex-end; height: auto; padding-bottom: 20px; border-radius: 20px; float: left; margin-bottom: 20px; background-color: #fff; text-align: center;">
                                <p class="pipe2" style="color: #b72a4a; font-size:18px; color: #8E94F2; font-weight: bold; line-height: 10px;">''' + promo1 + '''</p>
                                <img src="''' + images[0] + '''" width="204" height="204" alt="Odillia" style="max-width: 100%; height: auto;"/>
                                <p class="pipe1" style="color: #b72a4a; font-size:10px; color: #414243; font-weight: bold; line-height: 10px;">''' + captions[0] + '''</p>
                                <input type="button" name="button" id="button" value="COMPRA AHORA" class="btn" style="width: 225px; height: 40px; background-color: #354c82; border-radius: 10px; font-family: 'Albert Sans', sans-serif; font-size: 16px; font-weight: 600; color: #FFFFFF; cursor: pointer; border-width: 0px; border-style: none; text-align: center;">
                            </section>
                        </div>

                        <div class="div_2" style="width: 100%; display: inline-flex;">
                            <section class="producto_a" style="width: 48.80%; height: auto; margin-right: 1%; padding-bottom: 20px; border-radius: 20px; align-self: flex-end; float: left; margin-bottom: 20px; background-color: #fff; text-align: center;">
                                <p class="pipe2" style="color: #b72a4a; font-size:18px; color: #8E94F2; font-weight: bold; line-height: 10px;">''' + promo2 + '''</p>
                                <img src="''' + images[1] + '''" width="204" height="204" alt="Odillia" style="max-width: 100%; height: auto;"/>
                                <p class="pipe1" style="color: #b72a4a; font-size:10px; color: #414243; font-weight: bold; line-height: 10px;">''' + captions[1] + '''</p>
                                <input type="button" name="button" id="button" value="COMPRA AHORA" class="btn" style="width: 225px; height: 40px; background-color: #354c82; border-radius: 10px; font-family: 'Albert Sans', sans-serif; font-size: 16px; font-weight: 600; color: #FFFFFF; cursor: pointer; border-width: 0px; border-style: none; text-align: center;">
                            </section>
                        
                            <section class="producto_a1" style="width: 48.80%; height: auto; margin-left: 1%; padding-bottom: 20px; border-radius: 20px; align-self: flex-end; float: left; margin-bottom: 20px; background-color: #fff; text-align: center;">
                                <p class="pipe2" style="color: #b72a4a; font-size:18px; color: #8E94F2; font-weight: bold; line-height: 10px;">''' + promo3 + '''</p>
                                <img src="''' + images[2] + '''" width="204" height="204" alt="Odillia" style="max-width: 100%; height: auto;"/>
                                <p class="pipe1" style="color: #b72a4a; font-size:10px; color: #414243; font-weight: bold; line-height: 10px;">''' + captions[2] + '''</p>
                                <input type="button" name="button" id="button" value="COMPRA AHORA" class="btn" style="width: 225px; height: 40px; background-color: #354c82; border-radius: 10px; font-family: 'Albert Sans', sans-serif; font-size: 16px; font-weight: 600; color: #FFFFFF; cursor: pointer; border-width: 0px; border-style: none; text-align: center;">
                            </section>
                        </div>
                            
                        <div class="div_2" style="width: 100%; display: inline-flex;">
                            <section class="producto_a" style="width: 48.80%; height: auto; margin-right: 1%; padding-bottom: 20px; border-radius: 20px; align-self: flex-end; float: left; margin-bottom: 20px; background-color: #fff; text-align: center;">
                                <p class="pipe2" style="color: #b72a4a; font-size:18px; color: #8E94F2; font-weight: bold; line-height: 10px;">''' + promo4 + '''</p>
                                <img src="''' + images[3] + '''" width="204" height="204" alt="Odillia" style="max-width: 100%; height: auto;"/>
                                <p class="pipe1" style="color: #b72a4a; font-size:10px; color: #414243; font-weight: bold; line-height: 10px;">''' + captions[3] + '''</p>
                                <input type="button" name="button" id="button" value="COMPRA AHORA" class="btn" style="width: 225px; height: 40px; background-color: #354c82; border-radius: 10px; font-family: 'Albert Sans', sans-serif; font-size: 16px; font-weight: 600; color: #FFFFFF; cursor: pointer; border-width: 0px; border-style: none; text-align: center;">
                            </section>
                        
                            <section class="producto_a1" style="width: 48.80%; height: auto; margin-left: 1%; padding-bottom: 20px; border-radius: 20px; align-self: flex-end; float: left; margin-bottom: 20px; background-color: #fff; text-align: center;">
                                <p class="pipe2" style="color: #b72a4a; font-size:18px; color: #8E94F2; font-weight: bold; line-height: 10px;">''' + promo5 + '''</p>
                                <img src="''' + images[4] + '''" width="204" height="204" alt="Odillia" style="max-width: 100%; height: auto;"/>
                                <p class="pipe1" style="color: #b72a4a; font-size:10px; color: #414243; font-weight: bold; line-height: 10px;">''' + captions[4] + '''</p>
                                <input type="button" name="button" id="button" value="COMPRA AHORA" class="btn" style="width: 225px; height: 40px; background-color: #354c82; border-radius: 10px; font-family: 'Albert Sans', sans-serif; font-size: 16px; font-weight: 600; color: #FFFFFF; cursor: pointer; border-width: 0px; border-style: none; text-align: center;">
                            </section>
                        </div>

                        <div class="div_2" style="width: 100%; display: inline-flex;">
                            <section class="producto_a" style="width: 48.80%; height: auto; margin-right: 1%; padding-bottom: 20px; border-radius: 20px; align-self: flex-end; float: left; margin-bottom: 20px; background-color: #fff; text-align: center;">
                                <p class="pipe2" style="color: #b72a4a; font-size:18px; color: #8E94F2; font-weight: bold; line-height: 10px;">''' + promo6 + '''</p>
                                <img src="''' + images[5] + '''" width="204" height="204" alt="Odillia" style="max-width: 100%; height: auto;"/>
                                <p class="pipe1" style="color: #b72a4a; font-size:10px; color: #414243; font-weight: bold; line-height: 10px;">''' + captions[5] + '''</p>
                                <input type="button" name="button" id="button" value="COMPRA AHORA" class="btn" style="width: 225px; height: 40px; background-color: #354c82; border-radius: 10px; font-family: 'Albert Sans', sans-serif; font-size: 16px; font-weight: 600; color: #FFFFFF; cursor: pointer; border-width: 0px; border-style: none; text-align: center;">
                            </section>
                            
                            <section class="producto_a1" style="width: 48.80%; height: auto; margin-left: 1%; padding-bottom: 20px; border-radius: 20px; align-self: flex-end; float: left; margin-bottom: 20px; background-color: #fff; text-align: center;">
                                <p class="pipe2" style="color: #b72a4a; font-size:18px; color: #8E94F2; font-weight: bold; line-height: 10px;">''' + promo7 + '''</p>
                                <img src="''' + images[6] + '''" width="204" height="204" alt="Odillia" style="max-width: 100%; height: auto;"/>
                                <p class="pipe1" style="color: #b72a4a; font-size:10px; color: #414243; font-weight: bold; line-height: 10px;">''' + captions[6] + '''</p>
                                <input type="button" name="button" id="button" value="COMPRA AHORA" class="btn" style="width: 225px; height: 40px; background-color: #354c82; border-radius: 10px; font-family: 'Albert Sans', sans-serif; font-size: 16px; font-weight: 600; color: #FFFFFF; cursor: pointer; border-width: 0px; border-style: none; text-align: center;">
                            </section>
                        </div>

                        <section class="icons" style="width: 100%; height: auto; border-top-left-radius: 20px; border-top-right-radius: 20px; background-color: #ededed; text-align: center; float: left;">
                            <div  class="icon" style="width: 33.33%; height: auto; float: left;">
                                <img src="''' + iconos[0] + '''" width="278" height="186" alt="Odillia" style="max-width: 100%; height: auto;"/>
                            </div>
                            <div class="icon" style="width: 33.33%; height: auto; float: left;">
                                <img src="''' + iconos[1] + '''" width="277" height="186" alt="Odillia" style="max-width: 100%; height: auto;"/>
                            </div>
                            <div class="icon" style="width: 33.33%; height: auto; float: left;">
                                <img src="''' + iconos[2] + '''" width="279" height="186" alt="Odillia" style="max-width: 100%; height: auto;"/>
                            </div>
                            </section>

                        <section class="redes" style="width: 100%; height: auto; border-bottom-left-radius: 20px; border-bottom-right-radius: 20px; margin-bottom: 20px; background-color: #ededed; text-align: center; float: left;">
                            <img src="''' + redes[0] + '''" width="71" height="95" alt="Odillia"/>
                            <img src="''' + redes[1] + '''" width="71" height="95" alt="Odillia"/>
                            <img src="''' + redes[2] + '''" width="71" height="95" alt="Odillia"/>
                            <img src="''' + redes[3] + '''" width="69" height="95" alt="Odillia"/>
                        </section>
                        <section class="info" style="width: 834px; height: 172px; background-color: #ededed; font-family: 'Albert Sans', sans-serif; color: #7c7c7c; font-size: 23px; font-weight: 400; text-align: center; float: left; margin-bottom: 20px;">
                            <span class="unsuscribe" style="font-size: 15px; margin-top: 80px;">Si deseas cancelar el envío de promociones Odillia, <a href="#" class="liga2">haz clic aqu&iacute;</a></span>
                        </section>
                    </section>
                </body>
                </html>'''
    return html_code

streamlit_style = """
<style>
@import url('https://fonts.googleapis.com/css?family=Assistant');
@import url('https://fonts.googleapis.com/css?family=Albert+Sans');

html, body {
    font-family: 'Assistant'
}

.css-k1ih3n {
    padding: 1rem 2rem 5rem;
}

h1 {
    font-family: 'Albert Sans';
    font-size: 25px;
    font-weight: 600;
}

h2 {
    font-family: 'Albert Sans';
    font-size: 25px;
    font-weight: 600;
}

h3 {
    font-family: 'Albert Sans';
    font-size: 25px;
    font-weight: 600;
}

.streamlit-expander {
    border-radius: 2rem;
    background-color: #ffffff;
    color: #000000;
}

.streamlit-expanderHeader > div > p {
    font-size: 12px;
}

.streamlit-expander:hover > li > div > svg {
    border-radius: 2rem;
    background-color: #ffffff;
    fill: #000000;
}

#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-k1vhr4.egzxvld5 > div.block-container.css-91z34k.egzxvld4 > div:nth-child(1) > div > div > div > div:nth-child(13) > div:nth-child(4) > div:nth-child(1) > div > div:nth-child(2) > div > button {
    background-color: #ffffff;
    border-color: #ededed;
    display: block;
    width: 100%;
    cursor: pointer;
}

#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-k1vhr4.egzxvld5 > div.block-container.css-91z34k.egzxvld4 > div:nth-child(1) > div > div > div > div:nth-child(13) > div:nth-child(4) > div:nth-child(1) > div > div:nth-child(2) > div > button:active {
    background-color: #ffffff !important;
    border-color: #ededed;
    display: block;
    width: 100%;
    cursor: pointer;
}

#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-k1vhr4.egzxvld5 > div.block-container.css-91z34k.egzxvld4 > div:nth-child(1) > div > div > div > div:nth-child(13) > div:nth-child(4) > div:nth-child(1) > div > div:nth-child(2) > div > button:focus {
    background-color: #ffffff !important;
    border-color: #ededed;
    display: block;
    width: 100%;
    cursor: pointer;
}

#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-k1vhr4.egzxvld5 > div.block-container.css-91z34k.egzxvld4 > div:nth-child(1) > div > div > div > div:nth-child(13) > div:nth-child(4) > div:nth-child(1) > div > div:nth-child(2) > div > button > div > p {
    color: #000000;
    text-align: center;
}

#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-k1vhr4.egzxvld5 > div.block-container.css-91z34k.egzxvld4 > div:nth-child(1) > div > div > div > div:nth-child(13) > div:nth-child(4) > div:nth-child(1) > div > div:nth-child(2) > div > button:active > div > p {
    color: #000000;
    text-align: center;
}

.stButton {
    text-align: -webkit-center !important;
}

.stButton > button[kind='primary'] {
    background-color: #B72A4A;
    color: #ffffff;
    border-radius: 2rem;
    display: block;
    width: 100%;
    cursor: pointer;
    text-align: center;
    padding: 3px;
}

.stButton > button[kind='primary']:hover {
    border-color: transparent;
    background-color: #414243;
    color: #ffffff;
    background-repeat: no-repeat;
    background-position: left center;
    -webkit-appearance: none;
    width: 100%;
    cursor: pointer;
    text-align: center;
}

.stButton > button[kind='primary']:active {
    box-shadow: transparent 0px 0px 0px 0.2rem;
    border-color: transparent;
    background-color: #414243 !important;
}

.stButton > button[kind='primary']:focus {
    border-color: transparent;
    box-shadow: transparent 0px 0px 0px 0.2rem;
    background-color: #B72A4A;
    color: #ffffff;
    border-radius: 2rem;
    display: block;
    width: 100%;
    cursor: pointer;
    text-align: center;
}

.stButton > button[kind='primary'] > div > p {
    background-color: transparent;
    font-size: 15px;
    color: #ffffff;
    border-radius: 2rem;
    display: block;
    width: 100%;
    cursor: pointer;
    text-align: center;
}

.stButton > button[kind='primary']:hover > div > p {
    background-color: transparent;
    color: #ffffff;
    background-repeat: no-repeat;
    background-position: left center;
    -webkit-appearance: none;
    width: 100%;
    cursor: pointer;
    text-align: center;
}

.stButton > button[kind='primary']:active > div > p {
    box-shadow: transparent 0px 0px 0px 0.2rem;
    background-color: transparent !important;
}

.stButton > button[kind='primary']:focus > div > p {
    color: #ffffff;
    border-radius: 2rem;
    display: block;
    width: 100%;
    cursor: pointer;
    text-align: center;
}

.stButton > button[kind='secondary'] {
    background-color: #fff;
    color: #000;
    border-radius: 2rem;
    display: flex;
    align-self: center;
    width: 25%;
    cursor: pointer;
    padding: 3px;
}

.stButton > button[kind='secondary']:hover {
    border-color: transparent;
    background-color: #eee;
    color: #000;
    background-repeat: no-repeat;
    background-position: left center;
    -webkit-appearance: none;
    width: 25%;
    cursor: pointer;
    text-align: center;
}

.stButton > button[kind='secondary']:active {
    box-shadow: transparent 0px 0px 0px 0.2rem;
    border-color: transparent;
    background-color: #aaa !important;
}

.stButton > button[kind='secondary']:focus {
    border-color: #000;
    box-shadow: transparent 0px 0px 0px 0.2rem;
    background-color: #fff;
    color: #000;
    border-radius: 2rem;
    display: block;
    width: 25%;
    cursor: pointer;
    text-align: center;
}

.stButton > button[kind='secondary'] > div > p {
    background-color: transparent;
    font-size: 15px;
    color: #000;
    border-radius: 2rem;
    display: block;
    cursor: pointer;
    text-align: center;
}

.stButton > button[kind='secondary']:hover > div > p {
    background-color: transparent;
    color: #000;
    background-repeat: no-repeat;
    background-position: left center;
    -webkit-appearance: none;
    cursor: pointer;
    text-align: center;
}

.stButton > button[kind='secondary']:active > div > p {
    box-shadow: transparent 0px 0px 0px 0.2rem;
    background-color: transparent !important;
    color: #000;
}

.stButton > button[kind='secondary']:focus > div > p {
    color: #000;
    border-radius: 2rem;
    display: block;
    cursor: pointer;
    text-align: center;
}

#app {
    font-family: 'Assistant';
}

#root > div:nth-child(1) > div.withScreencast > div > div {
    background-image: url("https://raw.githubusercontent.com/PabloCaSan/Odillia/main/fondo.jpg");
    background-attachment: fixed;
    background-size: cover;
    background-position: left;
}

#root > div:nth-child(1) > div.withScreencast > div > div > header {
    height: 3px;
}

#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-k1vhr4.egzxvld5 > div.block-container.css-91z34k.egzxvld4 {
    padding: 1rem 3px 5rem;
}

img[src*="Odillia_Wordmark.jpg"] {
    width: 20% !important;
    align-self: end;
}

img[src*=".gif"] {
    width: 100% !important;
    align-self: center !important;
}

section[data-testid="stSidebar"] {
    background-color: #F0F2F6;
    color: #bb0a21;
    border-radius: 1rem;
    position: relative;
    height: 100%;
    width: 244px !important;
    overflow: overlay;
    transition: all 1s;
}

.stSelectbox > div > div {
    border-radius: 2rem;
    border-color: transparent;
}

.stSelectbox > div > div > div > div {
    padding-left: 10px;
}

.stMarkdown > div > p {
    color: #000000;
    text-align: center;
}

.stMarkdown > div > p > code {
    color: #000000;
    background: transparent;
    text-align: center;
}

.stTextInput > div {
    border-radius: 2rem;
    border-color: transparent;
}

.stTextInput > div > div > input {
    padding-left: 10px;
}

.element-container > iframe {
    border-radius: 1rem;
}

div[data-baseweb="popover"] {
    transition-duration: 0.5s;
    border-radius: 1rem;
}

div[data-baseweb="popover"] > div {
    border-radius: 1rem;
}

div[data-baseweb="popover"] > div > div > ul {
    border-radius: 1rem;
}

.css-184tjsw > p {
    font-size: 12px;
}

section[data-testid="stFileUploadDropzone"] {
    border-radius: 40px;
    background-color: #F2F8F7;
    font-size: 12px;
}

#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-k1vhr4.egzxvld5 > div.block-container.css-91z34k.egzxvld4 > div:nth-child(1) > div > div > ul > li > div.st-am.st-co.st-ci.st-cj.st-ck > div > div:nth-child(1) > div > div > div > section > button {
    border-radius: 40px;
    border-color: transparent;
}

.css-1aehpvj {
   font-size: 12px;
}

#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-k1vhr4.egzxvld5 > div.block-container.css-91z34k.egzxvld4 > div:nth-child(1) > div > div > div:nth-child(5) > div:nth-child(1) > div > div:nth-child(2) > div > button {
    background-color: #ffffff;
    border-color: #ededed;
    border-radius: 2rem;
    display: block;
    width: 100%;
    cursor: pointer;
    text-align: center;
    padding: 3px;
}

#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-k1vhr4.egzxvld5 > div.block-container.css-91z34k.egzxvld4 > div:nth-child(1) > div > div > div:nth-child(5) > div:nth-child(1) > div > div:nth-child(2) > div > button > div > p {
    font-size: 11px;
    color: #000000;
    border-color: #ededed;
}

#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-k1vhr4.egzxvld5 > div.block-container.css-91z34k.egzxvld4 > div:nth-child(1) > div > div > div:nth-child(5) > div:nth-child(1) > div > div:nth-child(2) > div > button:hover {
    border-color: #000000;
}

#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-k1vhr4.egzxvld5 > div.block-container.css-91z34k.egzxvld4 > div:nth-child(1) > div > div > div:nth-child(5) > div:nth-child(1) > div > div:nth-child(2) > div > button:active {
    background-color: #ededed !important;
}

#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-k1vhr4.egzxvld5 > div.block-container.css-k1ih3n.egzxvld4 > div:nth-child(1) > div > div > div:nth-child(5) > div:nth-child(1) > div > div:nth-child(2) > div > button {
    background-color: #ffffff;
    border-color: #ededed;
    border-radius: 2rem;
    display: block;
    width: 100%;
    cursor: pointer;
    text-align: center;
    padding: 3px;
}

#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-k1vhr4.egzxvld5 > div.block-container.css-k1ih3n.egzxvld4 > div:nth-child(1) > div > div > div:nth-child(5) > div:nth-child(1) > div > div:nth-child(2) > div > button > div > p {
    font-size: 11px;
    color: #000000;
    border-color: #ededed;
}

#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-k1vhr4.egzxvld5 > div.block-container.css-k1ih3n.egzxvld4 > div:nth-child(1) > div > div > div:nth-child(5) > div:nth-child(1) > div > div:nth-child(2) > div > button:hover {
    border-color: #000000;
}

#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-k1vhr4.egzxvld5 > div.block-container.css-k1ih3n.egzxvld4 > div:nth-child(1) > div > div > div:nth-child(5) > div:nth-child(1) > div > div:nth-child(2) > div > button:active {
    background-color: #ededed !important;
}

#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-k1vhr4.egzxvld5 > div.block-container.css-91z34k.egzxvld4 > div:nth-child(1) > div > div > div:nth-child(5) > div:nth-child(1) > div > div:nth-child(3) > div > button {
    background-color: #ffffff;
    border-color: #ededed;
    border-radius: 2rem;
    display: block;
    width: 100%;
    cursor: pointer;
    text-align: center;
    padding: 3px;
}

#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-k1vhr4.egzxvld5 > div.block-container.css-91z34k.egzxvld4 > div:nth-child(1) > div > div > div:nth-child(5) > div:nth-child(1) > div > div:nth-child(3) > div > button > div > p {
    font-size: 11px;
    color: #000000;
    border-color: #ededed;
}

#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-k1vhr4.egzxvld5 > div.block-container.css-91z34k.egzxvld4 > div:nth-child(1) > div > div > div:nth-child(5) > div:nth-child(1) > div > div:nth-child(3) > div > button:hover {
    border-color: #000000;
}

#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-k1vhr4.egzxvld5 > div.block-container.css-91z34k.egzxvld4 > div:nth-child(1) > div > div > div:nth-child(5) > div:nth-child(1) > div > div:nth-child(3) > div > button:active {
    background-color: #ededed !important;
}

#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-k1vhr4.egzxvld5 > div.block-container.css-k1ih3n.egzxvld4 > div:nth-child(1) > div > div > div:nth-child(5) > div:nth-child(1) > div > div:nth-child(3) > div > button {
    background-color: #ffffff;
    border-color: #ededed;
    border-radius: 2rem;
    display: block;
    width: 100%;
    cursor: pointer;
    text-align: center;
    padding: 3px;
}

#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-k1vhr4.egzxvld5 > div.block-container.css-k1ih3n.egzxvld4 > div:nth-child(1) > div > div > div:nth-child(5) > div:nth-child(1) > div > div:nth-child(3) > div > button > div > p {
    font-size: 11px;
    color: #000000;
    border-color: #ededed;
}

#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-k1vhr4.egzxvld5 > div.block-container.css-k1ih3n.egzxvld4 > div:nth-child(1) > div > div > div:nth-child(5) > div:nth-child(1) > div > div:nth-child(3) > div > button:hover {
    border-color: #000000;
}

#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-k1vhr4.egzxvld5 > div.block-container.css-k1ih3n.egzxvld4 > div:nth-child(1) > div > div > div:nth-child(5) > div:nth-child(1) > div > div:nth-child(3) > div > button:active {
    background-color: #ededed !important;
}

#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-k1vhr4.egzxvld5 > div.block-container.css-91z34k.egzxvld4 > div:nth-child(1) > div > div > div:nth-child(4) > div:nth-child(1) > div > div:nth-child(2) > div > button {
    background-color: #ffffff;
    border-color: #ededed;
    border-radius: 2rem;
    display: block;
    width: 100%;
    cursor: pointer;
    text-align: center;
    padding: 3px;
}

#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-k1vhr4.egzxvld5 > div.block-container.css-91z34k.egzxvld4 > div:nth-child(1) > div > div > div:nth-child(4) > div:nth-child(1) > div > div:nth-child(2) > div > button > div > p {
    font-size: 11px;
    color: #000000;
    border-color: #ededed;
}

#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-k1vhr4.egzxvld5 > div.block-container.css-91z34k.egzxvld4 > div:nth-child(1) > div > div > div:nth-child(4) > div:nth-child(1) > div > div:nth-child(2) > div > button:hover {
    border-color: #000000;
}

#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-k1vhr4.egzxvld5 > div.block-container.css-91z34k.egzxvld4 > div:nth-child(1) > div > div > div:nth-child(4) > div:nth-child(1) > div > div:nth-child(2) > div > button:active {
    background-color: #ededed !important;
}

#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-k1vhr4.egzxvld5 > div.block-container.css-k1ih3n.egzxvld4 > div:nth-child(1) > div > div > div:nth-child(4) > div:nth-child(1) > div > div:nth-child(2) > div > button {
    background-color: #ffffff;
    border-color: #ededed;
    border-radius: 2rem;
    display: block;
    width: 100%;
    cursor: pointer;
    text-align: center;
    padding: 3px;
}

#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-k1vhr4.egzxvld5 > div.block-container.css-k1ih3n.egzxvld4 > div:nth-child(1) > div > div > div:nth-child(4) > div:nth-child(1) > div > div:nth-child(2) > div > button > div > p {
    font-size: 11px;
    color: #000000;
    border-color: #ededed;
}

#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-k1vhr4.egzxvld5 > div.block-container.css-k1ih3n.egzxvld4 > div:nth-child(1) > div > div > div:nth-child(4) > div:nth-child(1) > div > div:nth-child(2) > div > button:hover {
    border-color: #000000;
}

#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-k1vhr4.egzxvld5 > div.block-container.css-k1ih3n.egzxvld4 > div:nth-child(1) > div > div > div:nth-child(4) > div:nth-child(1) > div > div:nth-child(2) > div > button:active {
    background-color: #ededed !important;
}


.streamlit-expanderHeader:hover > div > p {
    color: #B72A4A;
    font-weight: 600;
}

.streamlit-expanderHeader:hover > svg {
    fill: #B72A4A !important;
    scale: 1.1;
}

thead tr th:first-child {display:none}
tbody th {display:none}

div[data-testid="stTable"]{
    background-color: #ffffff;
}

.col_heading {
    color: #000000;
    font-weight: 700;
}

div[data-testid="stText"] {
    padding-top: 10px;
}

.stAlert > div {
    border-radius: 30px;
    background-color: #eefcf2;
}

</style>"""

st.markdown(streamlit_style, unsafe_allow_html=True)

def main():
    st.image(logo)
    
    ImagesPresentacion = ['None'
    ,'https://raw.githubusercontent.com/PabloCaSan/Odillia/main/ContenidoComercial_page-0002.jpg'
    ,'https://raw.githubusercontent.com/PabloCaSan/Odillia/main/ContenidoComercial_page-0003.jpg'
    ,'https://raw.githubusercontent.com/PabloCaSan/Odillia/main/ContenidoComercial_page-0009.jpg'
    ,'https://raw.githubusercontent.com/PabloCaSan/Odillia/main/ContenidoComercial_page-0010.jpg']

    def increment_counter():
        print(None)
        if st.session_state['count1'] < len(ImagesPresentacion)-1:
            st.session_state['count1'] += 1

    def decrement_counter():
        print(None)
        if st.session_state['count1'] > 1:
            st.session_state['count1'] -= 1

    st.image(ImagesPresentacion[st.session_state['count1']])

    cols1, cols2, cols3, cols4, cols5 = st.columns([1,1,1,1,1])
    with cols1:
        st.button('◀', on_click=decrement_counter, type='primary')
    with cols3:
        st.write(st.session_state['count1'], '/', len(ImagesPresentacion)-1)
    with cols5:
        st.button('▶', on_click=increment_counter, type='primary')

def RecomenderSystemDemo():

    if(st.session_state['page_change'] == 1):
        
        st.image(logo)

        st.markdown(""" <h1 style='color:#b52b4a'> Carga <span style='color:#414243'> de datos </span> """, unsafe_allow_html=True)

        st.session_state['selectedSegment'] = option_menu(None, ["Farmacia", "Supermercado", "Especialidad"], 
            icons=['bandaid', 'basket', 'mortarboard'], 
            menu_icon="grid-3x3-gap"
            ,styles={
            "container": {"background-color": "#f0f2f6", "border-radius": "2rem"},
            "icon": {"color": "#B72A4A", "font-size": "16px"}, 
            "nav-link": {"font-size": "12px", "text-align": "center", "margin":"2px","--hover-color": "#ffffff", "border-radius":"1rem", "transition":"0.5s", "font-weight":"600", "padding-bottom": "3px","padding-top": "3px"},
            "nav-link-selected": {"font-size": "12px", "background-color": "#000000", "border-radius":"1rem", "font-weight":"600"},
            }
            , orientation="horizontal"
            , default_index=0)

        with st.expander("a.    Historial de compras",expanded=False):
                FakeSTI = st.file_uploader("Cargue el historial de compras",label_visibility="hidden")
                if(FakeSTI is not None):
                    try:
                        try:
                            FakeSTI_df = pd.read_csv(FakeSTI, encoding='UTF-8-SIG').head(4)
                            st.dataframe(FakeSTI_df.astype('str'))
                        except:
                            FakeSTI_df = pd.read_csv(FakeSTI, encoding='ISO-8859-1').head(4)
                            st.dataframe(FakeSTI_df.astype('str'))
                    except:
                        st.write('El archivo fue cargado sin vista previa')
        
        with st.expander("b.    Catálogo de productos",expanded=False):
                FakeIL = st.file_uploader("Cargue el catálogo de productos",label_visibility="hidden")
                if(FakeIL is not None): 
                    try:
                        try:
                            FakeIL_df = pd.read_csv(FakeIL, encoding='UTF-8-SIG').head(4)
                            st.dataframe(FakeIL_df.astype('str'))
                        except:
                            FakeIL_df = pd.read_csv(FakeIL, encoding='ISO-8859-1').head(4)
                            st.dataframe(FakeIL_df.astype('str'))
                    except:
                        st.write('El archivo fue cargado sin vista previa')

        with st.expander("c.    Catálogo ecommerce",expanded=False):
                FakeILWL = st.file_uploader("Cargue la lista de enlaces a productos",label_visibility="hidden")
                if(FakeILWL is not None): 
                    try:
                        try:
                            FakeILWL_df = pd.read_csv(FakeILWL, encoding='UTF-8-SIG').head(4)
                            st.dataframe(FakeILWL_df.astype('str'))
                        except:
                            FakeILWL_df = pd.read_csv(FakeILWL, encoding='ISO-8859-1').head(4)
                            st.dataframe(FakeILWL_df.astype('str'))
                    except:
                        st.write('El archivo fue cargado sin vista previa')

        with st.expander("d.    Promociones",expanded=False):
                FakeOffers = st.file_uploader("Cargue la lista de promociones",label_visibility="hidden")
                if(FakeOffers is not None): 
                    try:
                        try:
                            FakeOffers_df = pd.read_csv(FakeOffers, encoding='UTF-8-SIG').head(4)
                            st.dataframe(FakeOffers_df.astype('str'))
                        except:
                            FakeOffers_df = pd.read_csv(FakeOffers, encoding='ISO-8859-1').head(4)
                            st.dataframe(FakeOffers_df.astype('str'))
                    except:
                        st.write('El archivo fue cargado sin vista previa')
        
        if(st.session_state['selectedSegment']=='Farmacia'):
            url_STI = 'https://raw.githubusercontent.com/PabloCaSan/Streamlit/main/FAhorro_SaleTransactionsItems_anon.csv'
            uploaded_STI = requests.get(url_STI, auth=(username,token), headers=headers).content
            try:
                st.session_state['STI'] = pd.read_csv(io.StringIO(uploaded_STI.decode('UTF-8-SIG')))
            except:
                st.session_state['STI'] = pd.read_csv(io.StringIO(uploaded_STI.decode('ISO-8859-1')))

            url_IL = 'https://raw.githubusercontent.com/PabloCaSan/Streamlit/main/FAhorro_ItemsList_anon.csv'
            uploaded_IL = requests.get(url_IL, auth=(username,token), headers=headers).content
            try:
                st.session_state['IL'] = pd.read_csv(io.StringIO(uploaded_IL.decode('UTF-8-SIG')))
            except:
                st.session_state['IL'] = pd.read_csv(io.StringIO(uploaded_IL.decode('ISO-8859-1')))
            
            url_ILWL = 'https://raw.githubusercontent.com/PabloCaSan/Streamlit/main/FAhorro_ItemsListWithLink_anon.csv'
            uploaded_ILWL = requests.get(url_ILWL, auth=(username,token), headers=headers).content
            try:
                st.session_state['SKULink'] = pd.read_csv(io.StringIO(uploaded_ILWL.decode('UTF-8-SIG')))
            except:
                st.session_state['SKULink'] = pd.read_csv(io.StringIO(uploaded_ILWL.decode('ISO-8859-1')))
            st.session_state['SKULink2'] = st.session_state['SKULink'].copy()
            st.session_state['SKULinkRaw'] = st.session_state['SKULink'].copy()

            url_Matrix = 'https://raw.githubusercontent.com/PabloCaSan/Streamlit/main/FAhorro_SimilarityMatrix_anon.csv'
            uploaded_Matrix = requests.get(url_Matrix, auth=(username,token), headers=headers).content
            try:
                st.session_state['Matrix'] = pd.read_csv(io.StringIO(uploaded_Matrix.decode('UTF-8-SIG')))
            except:
                st.session_state['Matrix'] = pd.read_csv(io.StringIO(uploaded_Matrix.decode('ISO-8859-1')))

            url_MatrixSegment = 'https://raw.githubusercontent.com/PabloCaSan/Streamlit/main/SimilarityMatrix_BySegment.csv'
            uploaded_MatrixSegment = requests.get(url_MatrixSegment, auth=(username,token), headers=headers).content
            try:
                st.session_state['MatrixSegment'] = pd.read_csv(io.StringIO(uploaded_MatrixSegment.decode('UTF-8-SIG')))
            except:
                st.session_state['MatrixSegment'] = pd.read_csv(io.StringIO(uploaded_MatrixSegment.decode('ISO-8859-1')))

            url_MatrixCategory = 'https://raw.githubusercontent.com/PabloCaSan/Streamlit/main/SimilarityMatrix_ByCategory.csv'
            uploaded_MatrixCategory = requests.get(url_MatrixCategory, auth=(username,token), headers=headers).content
            try:
                st.session_state['MatrixCategory'] = pd.read_csv(io.StringIO(uploaded_MatrixCategory.decode('UTF-8-SIG')))
            except:
                st.session_state['MatrixCategory'] = pd.read_csv(io.StringIO(uploaded_MatrixCategory.decode('ISO-8859-1')))
        
        if(st.session_state['selectedSegment']=='Supermercado'):
            url_STI = 'https://raw.githubusercontent.com/PabloCaSan/Streamlit/main/SK_SaleTransactionsItems_anon.csv'
            uploaded_STI = requests.get(url_STI, auth=(username,token), headers=headers).content
            try:
                st.session_state['STI'] = pd.read_csv(io.StringIO(uploaded_STI.decode('UTF-8-SIG')))
            except:
                st.session_state['STI'] = pd.read_csv(io.StringIO(uploaded_STI.decode('ISO-8859-1')))

            url_IL = 'https://raw.githubusercontent.com/PabloCaSan/Streamlit/main/SK_ItemsList_anon.csv'
            uploaded_IL = requests.get(url_IL, auth=(username,token), headers=headers).content
            try:
                st.session_state['IL'] = pd.read_csv(io.StringIO(uploaded_IL.decode('UTF-8-SIG')))
            except:
                st.session_state['IL'] = pd.read_csv(io.StringIO(uploaded_IL.decode('ISO-8859-1')))

            url_ILWL = 'https://raw.githubusercontent.com/PabloCaSan/Streamlit/main/SK_ItemsListWithLink_anon.csv'
            uploaded_ILWL = requests.get(url_ILWL, auth=(username,token), headers=headers).content
            try:
                st.session_state['SKULink'] = pd.read_csv(io.StringIO(uploaded_ILWL.decode('UTF-8-SIG')))
            except:
                st.session_state['SKULink'] = pd.read_csv(io.StringIO(uploaded_ILWL.decode('ISO-8859-1')))
            st.session_state['SKULink2'] = st.session_state['SKULink'].copy()
            st.session_state['SKULinkRaw'] = st.session_state['SKULink'].copy()

            url_Matrix = 'https://raw.githubusercontent.com/PabloCaSan/Streamlit/main/SK_SimilarityMatrix_anon.csv'
            uploaded_Matrix = requests.get(url_Matrix, auth=(username,token), headers=headers).content
            try:
                st.session_state['Matrix'] = pd.read_csv(io.StringIO(uploaded_Matrix.decode('UTF-8-SIG')))
            except:
                st.session_state['Matrix'] = pd.read_csv(io.StringIO(uploaded_Matrix.decode('ISO-8859-1')))

        if(st.session_state['selectedSegment']=='Especialidad'):
            url_STI = 'https://raw.githubusercontent.com/PabloCaSan/Streamlit/main/Probell_SaleTransactionsItems_anon.csv'
            uploaded_STI = requests.get(url_STI, auth=(username,token), headers=headers).content
            try:
                st.session_state['STI'] = pd.read_csv(io.StringIO(uploaded_STI.decode('UTF-8-SIG')))
            except:
                st.session_state['STI'] = pd.read_csv(io.StringIO(uploaded_STI.decode('ISO-8859-1')))

            url_IL = 'https://raw.githubusercontent.com/PabloCaSan/Streamlit/main/Probell_ItemsList_anon.csv'
            uploaded_IL = requests.get(url_IL, auth=(username,token), headers=headers).content
            try:
                st.session_state['IL'] = pd.read_csv(io.StringIO(uploaded_IL.decode('UTF-8-SIG')))
            except:
                st.session_state['IL'] = pd.read_csv(io.StringIO(uploaded_IL.decode('ISO-8859-1')))

            url_ILWL = 'https://raw.githubusercontent.com/PabloCaSan/Streamlit/main/Probell_ItemsListWithLink_anon.csv'
            uploaded_ILWL = requests.get(url_ILWL, auth=(username,token), headers=headers).content
            try:
                st.session_state['SKULink'] = pd.read_csv(io.StringIO(uploaded_ILWL.decode('UTF-8-SIG')))
            except:
                st.session_state['SKULink'] = pd.read_csv(io.StringIO(uploaded_ILWL.decode('ISO-8859-1')))
            st.session_state['SKULink2'] = st.session_state['SKULink'].copy()
            st.session_state['SKULinkRaw'] = st.session_state['SKULink'].copy()

            url_Matrix = 'https://raw.githubusercontent.com/PabloCaSan/Streamlit/main/Probell_SimilarityMatrix_anon.csv'
            uploaded_Matrix = requests.get(url_Matrix, auth=(username,token), headers=headers).content
            try:
                st.session_state['Matrix'] = pd.read_csv(io.StringIO(uploaded_Matrix.decode('UTF-8-SIG')))
            except:
                st.session_state['Matrix'] = pd.read_csv(io.StringIO(uploaded_Matrix.decode('ISO-8859-1')))

        if(uploaded_Matrix is not None and uploaded_IL is not None and uploaded_ILWL is not None and uploaded_STI):                    
            st.session_state['MatrixRaw'] = st.session_state['Matrix'].copy()
            st.session_state['MatrixRaw'] = st.session_state['MatrixRaw'].merge(st.session_state['IL'], how='inner', on='ItemSKU')
            st.session_state['MatrixRaw'] = st.session_state['MatrixRaw'].merge(st.session_state['IL'].rename(columns={'ItemSKU':'SimilarItemSKU', 'ItemName':'SimilarItemName'}), how='inner', on='SimilarItemSKU')
            st.session_state['MatrixRaw'] = st.session_state['MatrixRaw'][[
                'ItemSKU'
                , 'ItemName'
                ,'SimilarItemSKU'
                , 'SimilarItemName'
                , 'SimilarityScore'
            ]]
            st.session_state['MatrixRaw'].sort_values(by=['ItemSKU', 'SimilarityScore'], ascending=[True, False], inplace=True)

            st.session_state['Purchased_items_name_Raw'] = st.session_state['MatrixRaw'].ItemName.unique()
        cols1, cols2, cols3, cols4, cols5 = st.columns([1,1,1,1,1])
        with cols5:
            st.button('Iniciar I.A.',key='1>',on_click=next_page, type='primary')
             
    if(st.session_state['page_change'] == 2):
        with st.empty():            
            with st.container():
                st.image(logo)
                st.markdown(""" <h2 style='color:#8D8E91'> Analizando los datos... </h2>""", unsafe_allow_html=True)
                cols1, cols2, cols3 = st.columns([1,1,1])
                with cols2:
                    st.image('https://raw.githubusercontent.com/PabloCaSan/Odillia/main/generando_conocimiento.gif', use_column_width=True)
                time.sleep(5)
            with st.container():
                st.image(logo)
                st.markdown(""" <h2 style='color:#8D8E91'> Generando conocimiento... </h2>""", unsafe_allow_html=True)
                cols1, cols2, cols3 = st.columns([1,1,1])
                with cols2:
                    st.image('https://raw.githubusercontent.com/PabloCaSan/Odillia/main/analizando_datos.gif', use_column_width=True)
                time.sleep(5)
            with st.container():
                st.image(logo)
                st.markdown(""" <h2 style='color:#8D8E91'> ¡Recomendaciones generadas! </h2>""", unsafe_allow_html=True)
                cols1, cols2, cols3 = st.columns([1,1,1])
                with cols2:
                    st.image('https://raw.githubusercontent.com/PabloCaSan/Odillia/main/recomendaciones.gif', use_column_width=True)
                cols1, cols2, cols3 = st.columns([1,1,1])
                with cols1:
                    st.button('Carga de datos',key='<2',on_click=first_page, type='primary')
                with cols3:
                    st.button('Recomendaciones',key='2>',on_click=next_page, type='primary')

    if(st.session_state['page_change'] == 3):
        st.image(logo)
        st.title('Sistema de recomendaciones')
        STI = st.session_state['STI'].copy()
        IL = st.session_state['IL'].copy()
        SKULink = st.session_state['SKULink'].copy()
        SKULink2 = st.session_state['SKULink2'].copy()
        SKULinkRaw = st.session_state['SKULinkRaw'].copy()
        Matrix = st.session_state['Matrix'].copy()
        MatrixRaw = st.session_state['MatrixRaw'].copy()
        Purchased_items_name_Raw = st.session_state['Purchased_items_name_Raw'].copy()

        ILSimilar = IL[[
            'ItemSKU'
            ,'ItemName'
            ,'ItemCategory'
        ]]

        IL = IL[[
            'ItemSKU'
            ,'ItemName'
        ]]

        STI = STI.merge(IL,how='inner',on='ItemSKU')

        STI = STI[[
            'CardAffiliationId'
            , 'Name'
            , 'Description'
            , 'ItemSKU'
            , 'ItemName'
            , 'Quantity'
            , 'Price'
            , 'Amount'
            ,'SaleTransactionDate'
        ]]
                    
        st.session_state['selected2'] = option_menu(None, ["Por cliente", "Por carrito", "Por producto", "Por categoría", "Por segmento"], 
            icons=['person', 'cart', 'box-seam', 'columns', 'columns-gap'], 
            menu_icon="home"
            ,styles={
            "container": {"background-color": "#f0f2f6", "border-radius": "2rem"},
            "icon": {"color": "#B72A4A", "font-size": "16px"}, 
            "nav-link": {"font-size": "12px", "text-align": "center", "margin":"2px","--hover-color": "#ffffff", "border-radius":"1rem", "transition":"0.5s", "font-weight":"600", "padding-bottom": "3px","padding-bottom": "3px"},
            "nav-link-selected": {"font-size": "12px", "background-color": "#000000", "border-radius":"1rem"},
            }
            , orientation="horizontal")

        if (st.session_state['selected2']=='Por cliente'):
            st.title('Seleccione un cliente:')
            st.session_state['Description'] = st.selectbox(
                'Seleccione un cliente:',
                (st.session_state['STI'].Description.unique()),
                label_visibility="collapsed"
                ,on_change=hide_everything)
            
            st.session_state['Name'] = st.session_state['STI']['Name'][st.session_state['STI']['Description'] == st.session_state['Description']].values[0]
            Purchased_items = st.session_state['STI'][st.session_state['STI']['Description']==st.session_state['Description']].ItemSKU.unique()

            ForbbidenWords = [r'\bPROMO\b'
                              ,r'\bPROMOCION\b'
                              ,r'\bPAGO\b'
                              ,r'\bPAYNET\b'
                              ,r'\bRECARGA\b'
                              ,r'\bCOBRO\b'
                              ,r'\bPRMOCION\b'
                              ,r'\bTELCEL\b'
                              ,r'\bCFE\b'
                              ,r'\bBBVA\b'
                              ,r'\bBANAMEX\b'
                              ,r'\bBANORTE\b'
                              ,r'\bEL ROLLO\b'
                              ,r'\bBOLETO\b']
            
            STI_Percentage = STI.loc[(STI['Description']==st.session_state['Description'])&(~STI['ItemName'].astype('str').str.contains("|".join(ForbbidenWords)))].merge(st.session_state['IL'], on='ItemSKU', how='inner').groupby(by='ItemCategory').count().reset_index()[['ItemCategory','ItemSKU']].sort_values(by='ItemSKU', ascending=False).reset_index(drop=True)
            STI_Percentage['Perc'] = STI_Percentage['ItemSKU'].apply(lambda x: round(x/STI_Percentage['ItemSKU'].sum() * 100, 1))
            try:
                st.markdown(funnel_html(STI_Percentage.ItemCategory[0]
                                        ,str(STI_Percentage.Perc[0])
                                        ,STI_Percentage.ItemCategory[1]
                                        ,str(STI_Percentage.Perc[1])
                                        ,STI_Percentage.ItemCategory[2]
                                        ,str(STI_Percentage.Perc[2])
                                        ,STI_Percentage.ItemCategory[3]
                                        ,str(STI_Percentage.Perc[3])
                                        ,STI_Percentage.ItemCategory[4]
                                        ,str(STI_Percentage.Perc[4])), unsafe_allow_html=True)
            except:
                st.table(STI_Percentage[['ItemCategory','Perc']].rename(columns={"ItemCategory": "CATEGORIA", "Perc": "%"}))
            
            prepare_df = STI.loc[(STI['Description']==st.session_state['Description'])&(~STI['ItemName'].astype('str').str.contains("|".join(ForbbidenWords)))].reset_index(drop=True)
            prepare_df['Price'] = prepare_df['Price'].astype('int')
            prepare_df['Amount'] = prepare_df['Amount'].astype('int')
            prepare_df['SaleTransactionDate']= pd.to_datetime(prepare_df['SaleTransactionDate'])
            prepare_df['FirstPurchase'] = ''
            prepare_df['LastPurchase'] = ''
            for i in prepare_df.CardAffiliationId.unique():
                for j in prepare_df.ItemSKU.unique():
                    prepare_df['FirstPurchase'].loc[(prepare_df['CardAffiliationId']==i)&(prepare_df['ItemSKU']==j)] = prepare_df.loc[(prepare_df['CardAffiliationId']==i)&(prepare_df['ItemSKU']==j)].SaleTransactionDate.min()
            for i in prepare_df.CardAffiliationId.unique():
                for j in prepare_df.ItemSKU.unique():
                    prepare_df['LastPurchase'].loc[(prepare_df['CardAffiliationId']==i)&(prepare_df['ItemSKU']==j)] = prepare_df.loc[(prepare_df['CardAffiliationId']==i)&(prepare_df['ItemSKU']==j)].SaleTransactionDate.max()
            prepare_df['TimeInterval'] = prepare_df['LastPurchase'] - prepare_df['FirstPurchase']
            for i in range(0,len(prepare_df)):
                prepare_df['TimeInterval'][i] = prepare_df['TimeInterval'][i].days
            prepare_df['FrequencyPurchase'] = ''
            prepare_df['Units'] = ''
            prepare_df['AmountByProduct'] = ''
            for i in prepare_df.CardAffiliationId.unique():
                for j in prepare_df.ItemSKU.unique():
                    prepare_df['FrequencyPurchase'].loc[(prepare_df['CardAffiliationId']==i)&(prepare_df['ItemSKU']==j)] = prepare_df.loc[(prepare_df['CardAffiliationId']==i)&(prepare_df['ItemSKU']==j)].SaleTransactionDate.count()
            for i in prepare_df.CardAffiliationId.unique():
                for j in prepare_df.ItemSKU.unique():
                    prepare_df['Units'].loc[(prepare_df['CardAffiliationId']==i)&(prepare_df['ItemSKU']==j)] = prepare_df.loc[(prepare_df['CardAffiliationId']==i)&(prepare_df['ItemSKU']==j)].Quantity.sum()
            for i in prepare_df.CardAffiliationId.unique():
                for j in prepare_df.ItemSKU.unique():
                    prepare_df['AmountByProduct'].loc[(prepare_df['CardAffiliationId']==i)&(prepare_df['ItemSKU']==j)] = prepare_df.loc[(prepare_df['CardAffiliationId']==i)&(prepare_df['ItemSKU']==j)].Amount.sum()
            prepare_df2 = prepare_df.groupby(["CardAffiliationId", "ItemSKU"]).apply(lambda x: x.drop_duplicates("ItemSKU")).reset_index(drop=True).sort_values(by=['CardAffiliationId','ItemSKU'], ascending=[True,True])
            prepare_df2['TimeInterval'][prepare_df2['TimeInterval']==0] = 1
            prepare_df2['Score'] = prepare_df2['TimeInterval'] * prepare_df2['FrequencyPurchase'] * prepare_df2['Units'] * prepare_df2['AmountByProduct']

            Matrix = Matrix.merge(prepare_df2.drop(columns=['ItemName']), how='inner', on='ItemSKU')
            Matrix = Matrix.merge(IL, how='inner', on='ItemSKU')
            Matrix = Matrix.merge(ILSimilar.rename(columns={'ItemSKU':'SimilarItemSKU', 'ItemName':'SimilarItemName'}), how='inner', on='SimilarItemSKU').sort_values(by=['Quantity','SimilarityScore'], ascending=[False,False])
            Matrix = Matrix[[
                'ItemSKU'
                ,'ItemName'
                ,'Quantity'
                ,'SimilarItemSKU'
                ,'SimilarItemName'
                ,'SimilarityScore'
                ,'ItemCategory'
            ]][~Matrix['SimilarItemSKU'].isin(Purchased_items)]

            if(st.session_state['selectedSegment']!='Supermercado'):
                CustomerRecommendations = Matrix.groupby('ItemCategory').head(1)
            else:
                CustomerRecommendations = Matrix.groupby('ItemCategory').head(4)
            #CustomerRecommendations = CustomerRecommendations
            st.session_state['SendCustomerRecommendations'] = CustomerRecommendations[['SimilarItemName']].reset_index(drop=True).copy()

            cols1, cols2, cols3, cols4, cols5, cols6, cols7 = st.columns([1,1,1,1,1,1,1])                
            with cols4:
                st.write('\n')
                if(st.session_state['show_history'] == True):
                        st.button('Ocultar historial', on_click=hide_history, type='primary')
                else:
                    st.button('Mostrar historial', on_click=show_history, type='primary')    
                st.write('\n')

            if(st.session_state['show_history'] == True):
                st.table(STI.loc[(STI['Description']==st.session_state['Description'])&(~STI['ItemName'].astype('str').str.contains("|".join(ForbbidenWords)))].groupby(by=['ItemName']).sum().merge(ILSimilar, on='ItemName', how='inner').sort_values(by="Quantity", ascending=False).reset_index()[[
                'ItemName'
                ,'Quantity'
                ,'ItemCategory'
                ]].rename(columns={"ItemName": "PRODUCTO", "Quantity": "CANTIDAD"}))

            st.title('Recomendaciones')
            
            ShadowMerge = CustomerRecommendations.merge(SKULink, how='inner', on='SimilarItemSKU')

            images = ShadowMerge.ItemImgLink
            captions = ShadowMerge.SimilarItemName

            st.session_state['images_list'] = []
            st.session_state['captions_list'] = []

            for i in range(len(images)):
                st.session_state['images_list'].append(images[i])
                st.session_state['captions_list'].append(captions[i])
            
            if("Vitaminas" in st.session_state['Description']):
                st.session_state['consejo'] = ["Alimenta tu cuerpo con lo mejor, nuestros suplementos te ayudan a alcanzar tus metas de salud y bienestar"
                            ,"Transforma tu cuerpo desde adentro hacia afuera con nuestros poderosos suplementos alimenticios"
                            ,"Fortalece tu cuerpo y mente con nuestras vitaminas de alta calidad para una vida más saludable y feliz"]
            elif("Cardíacos" in st.session_state['Description']):
                st.session_state['consejo'] = ["Controla tu dieta, realiza ejercicio regularmente, y toma tus medicamentos según lo prescrito"
                            , "Evita el consumo excesivo de sal y alimentos procesados, y lleva un estilo de vida saludable"
                            ,"Mantén un peso saludable y consume una dieta rica en frutas, verduras y granos integrales"]
            elif("Diabetes" in st.session_state['Description']):
                st.session_state['consejo'] = ["Mantén un peso saludable, controla tu dieta y realiza ejercicio regularmente"
                            , "Controla regularmente tus niveles de azúcar en sangre y toma tus medicamentos según lo prescrito"
                            ,"Evita el consumo excesivo de azúcar y carbohidratos refinados, y lleva un estilo de vida saludable"]
            elif("Estomacal" in st.session_state['Description']):
                st.session_state['consejo'] = ["Mastica bien, evita comer en exceso y opta por alimentos saludables y no procesados"
                            , "Come despacio, mastica bien y evita alimentos grasosos y picantes."
                            ,"Bebe suficiente agua, come porciones pequeñas y evita acostarte justo después de comer"]
            elif("Bebé" in st.session_state['Description']):
                st.session_state['consejo'] = ["Mantén al bebé seguro, alimentado, limpio y en un ambiente cómodo y estimulante para su desarrollo"
                            , "Brinda amor, atención y contacto físico frecuente para fomentar el vínculo y el desarrollo emocional"
                            ,"Mantén al bebé alejado de objetos peligrosos, mantén la higiene y consulta a un pediatra regularmente"]
            elif("Cuidado Personal" in st.session_state['Description']):
                st.session_state['consejo'] = ["Bebe suficiente agua, usa protector solar y encuentra productos adecuados para tu tipo de piel"
                            , "Limpia tu piel antes de dormir, hidrátala diariamente y usa maquillaje de buena calidad"
                            ,"Mantén una dieta saludable, haz ejercicio regularmente y duerme lo suficiente para una piel radiante y saludable"]
            else:
                st.session_state['consejo'] = ["Descubre nuestras ofertas limitada y aprovecha los descuentos exclusivos. ¡Compra ahora y disfruta de nuestros productos!"
                            ,"¿Buscas calidad y buen precio? ¡Tenemos lo que necesitas! Compra ahora y sorpréndete con nuestros productos"
                            ,"Compra hoy y recibe envío gratis. ¡Aprovecha la oportunidad y haz tu pedido ahora!"]

            if(st.session_state['show_more'] == 14):
                try:
                    try:
                        components.html(html_CodeBlock_14(st.session_state['Name'] + '&#33;'
                                                    ,st.session_state['captions_list']
                                                    ,st.session_state['images_list']
                                                    ,"&#161;Hola "
                                                    ,st.session_state['consejo'][random.randint(0,2)]
                                                    ,st.session_state['promo'][random.randint(0,7)]
                                                    ,st.session_state['promo'][random.randint(0,7)]
                                                    ,st.session_state['promo'][random.randint(0,7)]
                                                    ,st.session_state['promo'][random.randint(0,7)]
                                                    ,st.session_state['promo'][random.randint(0,7)]
                                                    ,st.session_state['promo'][random.randint(0,7)]
                                                    ,st.session_state['promo'][random.randint(0,7)]
                                                    ,st.session_state['promo'][random.randint(0,7)]
                                                    ,st.session_state['promo'][random.randint(0,7)]
                                                    ,st.session_state['promo'][random.randint(0,7)]
                                                    ,st.session_state['promo'][random.randint(0,7)]
                                                    ,st.session_state['promo'][random.randint(0,7)]
                                                    ,st.session_state['promo'][random.randint(0,7)]
                                                    ,st.session_state['promo'][random.randint(0,7)])
                                                    ,height=3100)
                    except:
                        st.write("No hay suficientes recomendaciones para este producto, se muestran 7")
                        components.html(html_CodeBlock(st.session_state['Name'] + '&#33;'
                                                ,st.session_state['captions_list']
                                                ,st.session_state['images_list']
                                                ,"&#161;Hola "
                                                ,st.session_state['consejo'][random.randint(0,2)]
                                                ,st.session_state['promo'][random.randint(0,7)]
                                                ,st.session_state['promo'][random.randint(0,7)]
                                                ,st.session_state['promo'][random.randint(0,7)]
                                                ,st.session_state['promo'][random.randint(0,7)]
                                                ,st.session_state['promo'][random.randint(0,7)]
                                                ,st.session_state['promo'][random.randint(0,7)]
                                                ,st.session_state['promo'][random.randint(0,7)])
                                                ,height=2010)
                except:
                    st.write("No hay suficientes recomendaciones para este cliente o no se terminaron de cargar los datos")
            else:
                try:
                    components.html(html_CodeBlock(st.session_state['Name'] + '&#33;'
                                                ,st.session_state['captions_list']
                                                ,st.session_state['images_list']
                                                ,"&#161;Hola "
                                                ,st.session_state['consejo'][random.randint(0,2)]
                                                ,st.session_state['promo'][random.randint(0,7)]
                                                ,st.session_state['promo'][random.randint(0,7)]
                                                ,st.session_state['promo'][random.randint(0,7)]
                                                ,st.session_state['promo'][random.randint(0,7)]
                                                ,st.session_state['promo'][random.randint(0,7)]
                                                ,st.session_state['promo'][random.randint(0,7)]
                                                ,st.session_state['promo'][random.randint(0,7)])
                                                ,height=2010)
                except:
                    st.write("No hay suficientes recomendaciones para este cliente o no se terminaron de cargar los datos")

            cols1, cols2, cols3, cols4, cols5, cols6, cols7, cols8, cols9 = st.columns([1,1,1,1,1,1,1,1,1])                
            with cols5:
                st.write('\n')
                if(st.session_state['show_more'] == 14):
                    st.button('▲', on_click=show_less, type='primary')
                else:
                    st.button('▼', on_click=show_more, type='primary')    
                    
                if(st.session_state['show_list'] == True):
                    st.button('Ocultar lista', on_click=hide_list, type='primary')
                else:
                    st.button('Mostrar lista', on_click=show_list, type='primary')
                st.write('\n')

            if(st.session_state['show_list'] == True):
                cols1, cols2 = st.columns([1,1])                
                with cols1:
                    st.text('Integrar reglas de negocio')
                with cols2:
                    cols1, cols2, cols3, cols4, cols5 = st.columns([1,1,1,1,1])                
                    with cols1:
                        st.session_state['switch'] = tog.st_toggle_switch(label="", 
                            key="Key1", 
                            default_value=False, 
                            label_after = False, 
                            inactive_color = '#D3D3D3', 
                            active_color="#11567f", 
                            track_color="#29B5E8"
                            )

            if(st.session_state['switch'] == True):
                if(st.session_state['show_list'] == True):
                    st.table(CustomerRecommendations[[
                    'SimilarItemName'
                    ,'ItemCategory'
                    ]].reset_index(drop=True).rename(columns={"SimilarItemName": "PRODUCTO_SIMILAR", "ItemCategory": "CATEGORIA"}))
            else:
                if(st.session_state['show_list'] == True):
                    st.table(Matrix[[
                    'SimilarItemName'
                    ,'ItemCategory'
                    ]].reset_index(drop=True).rename(columns={"SimilarItemName": "PRODUCTO_SIMILAR", "ItemCategory": "CATEGORIA"}))
        
        if (st.session_state['selected2']=='Por carrito'):
            prevent_reloading = True
            st.title('Seleccione un producto:')

            producto_seleccionado = st.selectbox(
                'Seleccione un producto:',
                (Purchased_items_name_Raw),
                label_visibility="collapsed"
                ,on_change=hide_everything)
            col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
            with col5:
                add2cart = st.button('Agregar al carrito', type='primary')
            if add2cart == True:
                agregar_producto(producto_seleccionado)
                hide_everything()
                prevent_reloading = False
            st.title('Carrito')
            if(len(st.session_state['carrito_de_compras']) != 0):
                for i in list(set(st.session_state['carrito_de_compras'])):
                    col1, col2, col3, col4 = st.columns([1,1,1,1])
                    with col1:
                        remove = st.button('\-', key='-'+str(i), type='secondary')
                    with col4:
                        add = st.button('\+', key='+'+str(i), type='secondary')
                    if remove == True:
                        quitar_producto(st.session_state['carrito_de_compras'], i)
                        hide_everything()
                        prevent_reloading = True
                    if add == True:
                        agregar_producto(i)
                        hide_everything()
                        prevent_reloading = True
                    with col2:
                            if len([index for (index, item) in enumerate(st.session_state['carrito_de_compras']) if item == i]) != 0:
                                st.write(i)
                            else:
                                st.write('Producto eliminado')
                    with col3:
                            if len([index for (index, item) in enumerate(st.session_state['carrito_de_compras']) if item == i]) != 0:
                                st.write(len([index for (index, item) in enumerate(st.session_state['carrito_de_compras']) if item == i]))
            else:
                st.write('El carrito está vacío')
            st.session_state['carrito_de_compras_df'] = pd.DataFrame(st.session_state['carrito_de_compras'], columns=['Producto'])
            st.session_state['carrito_de_compras_df']['Cantidad'] = 1
            st.session_state['carrito_de_compras_df'] = st.session_state['carrito_de_compras_df'].groupby(by='Producto').sum().reset_index()
            if(len(st.session_state['carrito_de_compras']) != 0):
                st.title('Recomendaciones')
                cart_recommendations = st.session_state['carrito_de_compras_df'].rename(columns={'Producto':'ItemName'}).merge(st.session_state['IL'], on='ItemName')[['ItemName','ItemSKU','Cantidad']].merge(st.session_state['Matrix'],on='ItemSKU').sort_values(by=['Cantidad','SimilarityScore'], ascending=False).merge(st.session_state['IL'].rename(columns={'ItemSKU':'SimilarItemSKU','ItemName':'SimilarItemName','ItemCategory':'SimilarItemCategory'}), on='SimilarItemSKU').drop_duplicates(subset=['SimilarItemName'],keep='first').reset_index(drop=True)
                cart_recommendations = cart_recommendations[~cart_recommendations['SimilarItemName'].isin(list(set(st.session_state['carrito_de_compras'])))].reset_index(drop=True)
                cart_recommendations_1Category = cart_recommendations.groupby(by=['ItemName','SimilarItemCategory']).head(1).drop_duplicates(subset=['SimilarItemName'],keep='first').reset_index(drop=True)
                if(prevent_reloading==False):
                    with st.spinner('Estableciendo conexión con el servidor...'):
                        time.sleep(4)
                    success_message = st.success('Transferencia de datos completada con éxito')
                    time.sleep(2)
                    success_message.empty()
                success_message2 = st.success('Recomendaciones cargadas al sistema')
                time.sleep(1)
                success_message2.empty()
                if(len(cart_recommendations_1Category) > 7):
                    cart_recommendations_1Category = cart_recommendations_1Category.merge(st.session_state['SKULink'].rename(columns={'ItemSKU':'SimilarItemSKU'}), on='SimilarItemSKU')
                    images = cart_recommendations_1Category.ItemImgLink
                    captions = cart_recommendations_1Category.SimilarItemName
                    st.session_state['images_list3'] = []
                    st.session_state['captions_list3'] = []
                    for i in range(len(images)):
                        st.session_state['images_list3'].append(images[i])
                        st.session_state['captions_list3'].append(captions[i])
                else:
                    cart_recommendations = cart_recommendations.merge(st.session_state['SKULink'].rename(columns={'ItemSKU':'SimilarItemSKU'}), on='SimilarItemSKU')
                    images = cart_recommendations.ItemImgLink
                    captions = cart_recommendations.SimilarItemName
                    st.session_state['images_list3'] = []
                    st.session_state['captions_list3'] = []
                    for i in range(len(images)):
                        st.session_state['images_list3'].append(images[i])
                        st.session_state['captions_list3'].append(captions[i])
                if(st.session_state['show_more'] == 14):
                    try:
                        try:
                            components.html(html_CodeBlock_14(""
                                                            ,st.session_state['captions_list3']
                                                            ,st.session_state['images_list3']
                                                            ,"Complementa tu compra con estos productos"
                                                            ,"¡Aprovecha estos descuentos solo para ti!"
                                                            ,st.session_state['promo'][random.randint(0,7)]
                                                            ,st.session_state['promo'][random.randint(0,7)]
                                                            ,st.session_state['promo'][random.randint(0,7)]
                                                            ,st.session_state['promo'][random.randint(0,7)]
                                                            ,st.session_state['promo'][random.randint(0,7)]
                                                            ,st.session_state['promo'][random.randint(0,7)]
                                                            ,st.session_state['promo'][random.randint(0,7)]
                                                            ,st.session_state['promo'][random.randint(0,7)]
                                                            ,st.session_state['promo'][random.randint(0,7)]
                                                            ,st.session_state['promo'][random.randint(0,7)]
                                                            ,st.session_state['promo'][random.randint(0,7)]
                                                            ,st.session_state['promo'][random.randint(0,7)]
                                                            ,st.session_state['promo'][random.randint(0,7)]
                                                            ,st.session_state['promo'][random.randint(0,7)])
                                                            ,height=3100)
                        except:
                            st.write("No hay suficientes recomendaciones para este producto, se muestran 7")
                            components.html(html_CodeBlock(""
                                                        ,st.session_state['captions_list3']
                                                        ,st.session_state['images_list3']
                                                        ,"Complementa tu compra con estos productos"
                                                        ,"¡Aprovecha estos descuentos solo para ti!"
                                                        ,st.session_state['promo'][random.randint(0,7)]
                                                        ,st.session_state['promo'][random.randint(0,7)]
                                                        ,st.session_state['promo'][random.randint(0,7)]
                                                        ,st.session_state['promo'][random.randint(0,7)]
                                                        ,st.session_state['promo'][random.randint(0,7)]
                                                        ,st.session_state['promo'][random.randint(0,7)]
                                                        ,st.session_state['promo'][random.randint(0,7)])
                                                        ,height=2010)
                    except:
                        st.write("No hay suficientes recomendaciones para este producto")
                else:
                    try:
                        components.html(html_CodeBlock(""
                                                        ,st.session_state['captions_list3']
                                                        ,st.session_state['images_list3']
                                                        ,"Complementa tu compra con estos productos"
                                                        ,"¡Aprovecha estos descuentos solo para ti!"
                                                        ,st.session_state['promo'][random.randint(0,7)]
                                                        ,st.session_state['promo'][random.randint(0,7)]
                                                        ,st.session_state['promo'][random.randint(0,7)]
                                                        ,st.session_state['promo'][random.randint(0,7)]
                                                        ,st.session_state['promo'][random.randint(0,7)]
                                                        ,st.session_state['promo'][random.randint(0,7)]
                                                        ,st.session_state['promo'][random.randint(0,7)])
                                                        ,height=2010)
                    except:
                        st.write("No hay suficientes recomendaciones para este producto")
                    
                cols1, cols2, cols3, cols4, cols5, cols6, cols7, cols8, cols9 = st.columns([1,1,1,1,1,1,1,1,1])
                with cols5:
                    st.write('\n')
                    if(st.session_state['show_more'] > 7):
                        st.button('▲', on_click=show_less, type='primary')
                    else:
                        st.button('▼', on_click=show_more, type='primary')

                    if(st.session_state['show_list'] == True):
                        st.button('Ocultar lista', on_click=hide_list, type='primary')
                    else:
                        st.button('Mostrar lista', on_click=show_list, type='primary')   
                    st.write('\n')
                if(st.session_state['show_list'] == True):
                    if(len(cart_recommendations_1Category) > 7):
                        st.table(cart_recommendations_1Category[['SimilarItemName','SimilarItemCategory']].rename(columns={'SimilarItemName':'NOMBRE', 'SimilarItemCategory':'CATEGORIA'}))
                    else:
                        st.table(cart_recommendations[['SimilarItemName','SimilarItemCategory']].rename(columns={'SimilarItemName':'NOMBRE', 'SimilarItemCategory':'CATEGORIA'}))
            
        if (st.session_state['selected2']=='Por producto'):
            st.title('Seleccione un producto:')

            st.session_state['option2'] = st.selectbox(
                'Seleccione un producto:',
                (Purchased_items_name_Raw),
                label_visibility="collapsed"
                ,on_change=hide_everything)

            ProductRecommendations = MatrixRaw[MatrixRaw['ItemName']==st.session_state['option2']].sort_values(by='SimilarityScore', ascending=False)
            ShadowMerge2 = ProductRecommendations.merge(SKULink2, how='inner', on='SimilarItemSKU')

            images2 = ShadowMerge2.ItemImgLink
            captions2 = ShadowMerge2.SimilarItemName

            st.session_state['images_list2'] = []
            st.session_state['captions_list2'] = []

            for i in range(len(images2)):
                st.session_state['images_list2'].append(images2[i])
                st.session_state['captions_list2'].append(captions2[i])

            ShadowMerge2 = ShadowMerge2[[
                'ItemSKU'
                ,'ItemName'
                ,'SimilarItemSKU'
                ,'SimilarItemName'
                ,'SimilarityScore'
            ]]

            if(st.session_state['show_more'] == 14):
                try:
                    try:
                        components.html(html_CodeBlock_14(st.session_state['option2']
                                                    ,st.session_state['captions_list2']
                                                    ,st.session_state['images_list2']
                                                    ,""
                                                    ,"Si te gustó &#161;Te encantarán estos productos&#33;"
                                                    ,st.session_state['promo'][random.randint(0,7)]
                                                    ,st.session_state['promo'][random.randint(0,7)]
                                                    ,st.session_state['promo'][random.randint(0,7)]
                                                    ,st.session_state['promo'][random.randint(0,7)]
                                                    ,st.session_state['promo'][random.randint(0,7)]
                                                    ,st.session_state['promo'][random.randint(0,7)]
                                                    ,st.session_state['promo'][random.randint(0,7)]
                                                    ,st.session_state['promo'][random.randint(0,7)]
                                                    ,st.session_state['promo'][random.randint(0,7)]
                                                    ,st.session_state['promo'][random.randint(0,7)]
                                                    ,st.session_state['promo'][random.randint(0,7)]
                                                    ,st.session_state['promo'][random.randint(0,7)]
                                                    ,st.session_state['promo'][random.randint(0,7)]
                                                    ,st.session_state['promo'][random.randint(0,7)])
                                                    ,height=3100)
                    except:
                        st.write("No hay suficientes recomendaciones para este producto, se muestran 7")
                        components.html(html_CodeBlock(st.session_state['option2']
                                                ,st.session_state['captions_list2']
                                                ,st.session_state['images_list2']
                                                ,""
                                                ,"Otros clientes también compraron"
                                                ,st.session_state['promo'][random.randint(0,7)]
                                                ,st.session_state['promo'][random.randint(0,7)]
                                                ,st.session_state['promo'][random.randint(0,7)]
                                                ,st.session_state['promo'][random.randint(0,7)]
                                                ,st.session_state['promo'][random.randint(0,7)]
                                                ,st.session_state['promo'][random.randint(0,7)]
                                                ,st.session_state['promo'][random.randint(0,7)])
                                                ,height=2010)
                except:
                    st.write("No hay suficientes recomendaciones para este producto o no se terminaron de cargar los datos")
            else:
                try:
                    components.html(html_CodeBlock(st.session_state['option2']
                                                ,st.session_state['captions_list2']
                                                ,st.session_state['images_list2']
                                                ,""
                                                ,"Otros clientes también compraron"
                                                ,st.session_state['promo'][random.randint(0,7)]
                                                ,st.session_state['promo'][random.randint(0,7)]
                                                ,st.session_state['promo'][random.randint(0,7)]
                                                ,st.session_state['promo'][random.randint(0,7)]
                                                ,st.session_state['promo'][random.randint(0,7)]
                                                ,st.session_state['promo'][random.randint(0,7)]
                                                ,st.session_state['promo'][random.randint(0,7)])
                                                ,height=2010)
                except:
                    st.write("No hay suficientes recomendaciones para este producto o no se terminaron de cargar los datos")

            cols1, cols2, cols3, cols4, cols5, cols6, cols7, cols8, cols9 = st.columns([1,1,1,1,1,1,1,1,1])
            with cols5:
                st.write('\n')
                if(st.session_state['show_more'] > 7):
                    st.button('▲', on_click=show_less, type='primary')
                else:
                    st.button('▼', on_click=show_more, type='primary')

                if(st.session_state['show_list'] == True):
                    st.button('Ocultar lista', on_click=hide_list, type='primary')
                else:
                    st.button('Mostrar lista', on_click=show_list, type='primary')   
                st.write('\n')
            if(st.session_state['show_list'] == True):
                st.table(ShadowMerge2[[
                    'SimilarItemName'
                ]].reset_index(drop=True).rename(columns={"SimilarItemName": "PRODUCTO_SIMILAR"}))

        if (st.session_state['selected2']=='Por categoría'):
            
            Categories = st.session_state['MatrixCategory'].CategoryName.unique()

            st.title('Seleccione una categoría:')

            optionMC = st.selectbox(
                'Seleccione una categoría:',
                (Categories),
                label_visibility="collapsed"
                ,on_change=hide_everything)

            if(st.session_state['show_more'] == 14):
                st.dataframe(st.session_state['MatrixCategory'][st.session_state['MatrixCategory']['CategoryName']==optionMC].sort_values(by='SimilarityScore', ascending=False)[['RecommendedCategoryName']].reset_index(drop=True).rename(columns={"RecommendedCategoryName": "CATEGORIA_SIMILAR"}))
            else:
                st.dataframe(st.session_state['MatrixCategory'][st.session_state['MatrixCategory']['CategoryName']==optionMC].sort_values(by='SimilarityScore', ascending=False)[['RecommendedCategoryName']].reset_index(drop=True).head(7).rename(columns={"RecommendedCategoryName": "CATEGORIA_SIMILAR"}))
            
            cols1, cols2, cols3, cols4, cols5, cols6, cols7, cols8, cols9 = st.columns([1,1,1,1,1,1,1,1,1])
            with cols5:
                st.write('\n')
                if(st.session_state['show_more'] > 7):
                    st.button('▲', on_click=show_less, type='primary')
                else:
                    st.button('▼', on_click=show_more, type='primary')
                st.write('\n')

        if (st.session_state['selected2']=='Por segmento'):
            
            Segments = st.session_state['MatrixSegment'].SegmentName.unique()

            st.title('Seleccione un segmento:')

            optionMS = st.selectbox(
                'Seleccione un segmento:',
                (Segments),
                label_visibility="collapsed"
                ,on_change=hide_everything)

            if(st.session_state['show_more'] == 14):
                st.dataframe(st.session_state['MatrixSegment'][st.session_state['MatrixSegment']['SegmentName']==optionMS].sort_values(by='SimilarityScore', ascending=False)[['RecommendedSegmentName']].reset_index(drop=True).rename(columns={"RecommendedSegmentName": "SEGMENTO_SIMILAR"}))
            else:
                st.dataframe(st.session_state['MatrixSegment'][st.session_state['MatrixSegment']['SegmentName']==optionMS].sort_values(by='SimilarityScore', ascending=False)[['RecommendedSegmentName']].reset_index(drop=True).head(7).rename(columns={"RecommendedSegmentName": "SEGMENTO_SIMILAR"}))
            
            cols1, cols2, cols3, cols4, cols5, cols6, cols7, cols8, cols9 = st.columns([1,1,1,1,1,1,1,1,1])
            with cols5:
                st.write('\n')
                if(st.session_state['show_more'] > 7):
                    st.button('▲', on_click=show_less, type='primary')
                else:
                    st.button('▼', on_click=show_more, type='primary')
                st.write('\n')

        cols1, cols2, cols3= st.columns([1,1,1])
        with cols1:
            st.button('Carga de datos',key='<3',on_click=first_page, type='primary')
        with cols3:
            st.button('Envío',key='3>',on_click=next_page, type='primary')

    if(st.session_state['page_change'] == 4):
        st.image(logo)
        st.title('Envío de recomendaciones')
        st.session_state['selected3'] = option_menu(None, ["Email", "SMS", "Whatsapp", "Sucursal", "Otros"], 
            icons=['envelope', 'chat', 'whatsapp', 'shop', 'globe'], 
            menu_icon="home"
            ,styles={
            "container": {"background-color": "#f0f2f6", "border-radius": "2rem"},
            "icon": {"color": "#B72A4A", "font-size": "16px"}, 
            "nav-link": {"font-size": "12px", "text-align": "center", "margin":"2px","--hover-color": "#ffffff", "border-radius":"1rem", "transition":"0.5s", "font-weight":"600", "padding-bottom": "3px","padding-bottom": "3px"},
            "nav-link-selected": {"font-size": "12px", "background-color": "#000000", "border-radius":"1rem"},
            }
            , orientation="horizontal")

        if(st.session_state['selected3']=='Email'):
            st.header('Escriba su email')
            st.session_state['destinatario'] = st.text_input('', 'alguien@email.com')

        if(st.session_state['selected3']=='SMS'):
            st.header('Escriba su número telefónico')
            st.session_state['numero'] = st.text_input('', '0123456789')

        if(st.session_state['selected3']=='Whatsapp'):
            st.markdown(' <h3> Versión beta: </h3>', unsafe_allow_html=True)
            st.markdown(""" <b> Envíe el mensaje <i style='color:#B72A4A'> "join must-someone" </i> al <i style='color:#B72A4A'> +1 415 523 8886 </i>""", unsafe_allow_html=True)
            st.header('Escriba su número telefónico')
            st.session_state['numero'] = st.text_input('', '0123456789')
        if(st.session_state['selected3']=='Sucursal'):
            st.markdown('<b> <p style="text-align-last: start;"> Ponte en contacto con nosotros para saber cómo integrarlo </p> </b>',unsafe_allow_html=True)
            st.markdown('<b> <p style="color:#2EB6CB; text-align: right;"> helpdesk@odilliatech.com </p> </b>',unsafe_allow_html=True)

        if(st.session_state['selected3']=='Otros'):
            st.markdown('<b> <p style="text-align-last: start;"> Odillia se adapta a tus necesidades, ponte en contacto con nosotros </p> </b>',unsafe_allow_html=True)
            st.markdown('<b> <p style="color:#2EB6CB; text-align: right;"> helpdesk@odilliatech.com </p> </b>',unsafe_allow_html=True)

        cols1, cols2, cols3= st.columns([1,1,1])
        with cols1:
            st.button('Recomendaciones',key='<4',on_click=previous_page, type='primary')
        with cols3:
            st.button('Enviar',key='send',on_click=final_page, type='primary')

    if(st.session_state['page_change'] == 5):
        st.image(logo)
        st.title('¡Recomendaciones enviadas!')
        cols1, cols2, cols3 = st.columns([1,1,1])
        with cols2:
            st.image('https://raw.githubusercontent.com/PabloCaSan/Odillia/main/envio.gif', use_column_width=True)
        cols1, cols2, cols3= st.columns([1,1,1])
        with cols1:
            st.button('Envío',key='<5',on_click=previous_page, type='primary')

def CampaignReportDemo():
    st.image(logo)

    ImagesReport = [None
    ,'https://raw.githubusercontent.com/PabloCaSan/Odillia/main/ContenidoComercial_page-0012.jpg'
    ,'https://raw.githubusercontent.com/PabloCaSan/Odillia/main/ContenidoComercial_page-0013.jpg'
    ,'https://raw.githubusercontent.com/PabloCaSan/Odillia/main/ContenidoComercial_page-0014.jpg'
    ,'https://raw.githubusercontent.com/PabloCaSan/Odillia/main/ContenidoComercial_page-0015.jpg']

    def increment_counter():
        print(None)
        if st.session_state['count2'] < len(ImagesReport)-1:
            st.session_state['count2'] += 1

    def decrement_counter():
        print(None)
        if st.session_state['count2'] > 1:
            st.session_state['count2'] -= 1

    st.image(ImagesReport[st.session_state['count2']])

    columns1, columns2, columns3, columns4, columns5 = st.columns([1,1,1,1,1])

    with columns1:
        st.button('◀', on_click=decrement_counter, type='primary')
    with columns3:
        st.write(st.session_state['count2'], '/', len(ImagesReport)-1)
    with columns5:
        st.button('▶', on_click=increment_counter, type='primary')

def FareDemo():
    st.image(logo)
    
    ImagesFare = [None
    , 'https://raw.githubusercontent.com/PabloCaSan/Odillia/main/Diapositiva3.JPG'
    ,'https://raw.githubusercontent.com/PabloCaSan/Odillia/main/Diapositiva5.JPG']

    def increment_counter():
        print(None)
        if st.session_state['count3'] < len(ImagesFare)-1:
            st.session_state['count3'] += 1

    def decrement_counter():
        print(None)
        if st.session_state['count3'] > 1:
            st.session_state['count3'] -= 1

    st.image(ImagesFare[st.session_state['count3']])

    columns1, columns2, columns3, columns4, columns5 = st.columns([1,1,1,1,1])

    with columns1:
        st.button('◀', on_click=decrement_counter, type='primary')
    with columns3:
        st.write(st.session_state['count3'], '/', len(ImagesFare)-1)
    with columns5:
        st.button('▶', on_click=increment_counter, type='primary')

page_names_to_funcs = {
    "¿Qué es?": main,
    "Demo I.A.": RecomenderSystemDemo,
    "Beneficios": CampaignReportDemo,
    "Tarifas": FareDemo,
}

SideBar = st.sidebar
#SideBar.image(logo)

with SideBar:
    selected = option_menu("Menú"
    , ["¿Qué es?", 'Demo I.A.', 'Beneficios']
    , icons=[
        'easel'
        , 'robot'
        , 'graph-up-arrow'
        ]
        , menu_icon="none"
        ,styles={
            "menu-title": {"font-size": "15px", "font-weight":"600", "margin-left":"3px", "margin-right":"3px", "align-self": "center"},
            "container": {"background-color": "#F6F6F6", "border-radius": "1rem"},
            "icon": {"color": "#B72A4A", "font-size": "16px"}, 
            "nav-link": {"font-size": "12px", "text-align": "left", "margin":"2px","--hover-color": "#ffffff", "border-radius":"2rem", "transition":"0.5s", "font-weight":"600", "padding-top": "0.5rem", "padding-top": "0.5rem"},
            "nav-link-selected": {"font-size": "12px", "background-color": "#000000", "border-radius":"2rem", "font-weight":"600"},
        })


page_names_to_funcs[selected]()

