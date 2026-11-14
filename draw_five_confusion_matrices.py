from pathlib import Path
import json,textwrap
from PIL import Image,ImageDraw,ImageFont
R=Path('E:/BT1/output/word/v1_five_models')
records=json.loads((R/'verified_metrics.json').read_text(encoding='utf-8'))
im=Image.new('RGB',(2700,1850),'white');dr=ImageDraw.Draw(im)
def font(n):return ImageFont.truetype('C:/Windows/Fonts/arial.ttf',n)
def text(x,y,t,n=32,color='#18344D',center=False):
 if center:
  bb=dr.textbbox((0,0),t,font=font(n));x-=(bb[2]-bb[0])/2
 dr.text((x,y),t,font=font(n),fill=color)
text(1350,25,'MA TRẬN NHẦM LẪN CỦA NĂM MÔ HÌNH V1',48,center=True)
text(1350,90,'Tập xác thực: 1.277 bình luận, gồm 1.194 non-toxic và 83 toxic',33,center=True)
positions=[(15,170),(915,170),(1815,170),(465,870),(1365,870)]
for rec,(x,y) in zip(records,positions):
 name=rec['model'].replace(' V1 tại ngưỡng 0,52',' (ngưỡng 0,52)')
 text(x+435,y,name,37,center=True)
 text(x+435,y+62,'Nhãn dự đoán',29,center=True)
 gx=x+200;gy=y+160;size=230
 for j,t in enumerate(['Non-toxic (0)','Toxic (1)']):text(gx+size*(j+.5),y+110,t,28,center=True)
 for i,t in enumerate(['Non-toxic (0)','Toxic (1)']):text(x+12,gy+size*(i+.5)-20,t,26)
 for i in range(2):
  for j in range(2):
   value=rec[['tn','fp','fn','tp'][i*2+j]];v=value/1194
   color=tuple(int(a-b*v) for a,b in [(235,180),(243,130),(251,85)])
   xx=gx+j*size;yy=gy+i*size
   dr.rectangle((xx,yy,xx+size,yy+size),fill=color,outline='white',width=5)
   fg='white' if v>.65 else '#18344D'
   text(xx+size/2,yy+62,str(value),58,fg,True)
   text(xx+size/2,yy+135,[['TN','FP'],['FN','TP']][i][j],31,fg,True)
 assert sum(rec[k] for k in ['tn','fp','fn','tp'])==1277
text(1350,1545,'Hàng: nhãn thật  |  Cột: nhãn dự đoán  |  Các mô hình dùng cùng thang màu',29,center=True)
dr.line((100,1610,2600,1610),fill='#D9E1E8',width=2)
comment='Nhận xét chung: TF-IDF + SVM phát hiện nhiều câu toxic nhất (45/83) nhưng cũng báo nhầm nhiều nhất (97 câu). PhoBERT phát hiện 37/83 câu toxic, báo nhầm 56 câu và đạt Macro-F1 cao nhất trong năm mô hình. TF-IDF + Naive Bayes gần như chỉ dự đoán non-toxic, bỏ sót 82/83 câu toxic.'
for i,line in enumerate(textwrap.wrap(comment,width=139)):
 text(100,1640+i*48,line,32)
out=R/'V1_NAM_CONFUSION_MATRIX_CHUNG.png';im.save(out,dpi=(300,300));print(out)
