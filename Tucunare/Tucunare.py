import cv2
#importação do opencv

#tira o centro do contorno
def center(x, y, l, a):
    x1 = int(l / 2) #largura
    y1 = int(a / 2) # altura
    cx = x + x1 #tirar centro
    cy = y + y1
    return cx,cy
#estou chamando o vídeo
cap = cv2.VideoCapture('tucunare.mp4')

#background do opencv
tuc = cv2.createBackgroundSubtractorMOG2()
#detectando começando com 0 assim acumulando
detectando = []
#adicionando linha
posL = 200

offset = 400
#posição da lonha
xy1 = (800, posL)
xy2 = (20, posL)


total = 0

cima = 0
baixo = 0
while 1:
      #retorno do video
    ret, frame = cap.read()
#conversão do framework para cinza.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #tirar a diferença de um frame
    fgmask = tuc.apply(gray)

    #limpando a mascara ficando mais clean
    retval, tucu = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)


    #usar o opening assim limpar as camadas e karnel para reconhecer
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    #limpar as mascaras
    opening = cv2.morphologyEx(tucu, cv2.MORPH_OPEN, kernel, iterations = 4)

    #aumentar o tamanho da interação
    dilation = cv2.dilate(opening,kernel,iterations = 8)

    #indentifica o objeto e tras uma unica imagem fechando os espaços
    closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel, iterations = 9)
    cv2.imshow("closing", closing)
#Adionando linha do meio
    cv2.line(frame,xy1,xy2,(255,0,0),20)

    #tirar o contornos
    contours, hierarchy = cv2.findContours(dilation,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #contando o id
    i = 0
    # for tirar o tamanho e area dele. x e y aonde contorno começa w  e h altura e largura
    for cnt in contours:
        #calculando o retangulo da area
        (x,y,l,a) = cv2.boundingRect(cnt)
        #calculando a area total.
        area = cv2.contourArea(cnt)

        #grandes objetos tamanho
        if int(area) > 3150 :
            #criando o centro
            centro = center(x, y, l, a)

            #chamando o id
            cv2.putText(frame, str(i), (x+5, y+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255),2)
             #chamando um circulo
            cv2.circle(frame, centro, 7, (0, 0,255), -1)
             #tirar contorno do x e y, assim criando um detector
            cv2.rectangle(frame,(x,y),(x+l,y+a),(0,255,0),5)

           #identificando o objeto assim criando array
            if len(detectando) <= i:
                detectando.append([])
              #adiciona a partir do meio
            if centro[1]> posL-offset and centro[1] < posL+offset:
                detectando[i].append(centro)
            else:
                detectando[i].clear()
            #adicionando objeto.
            i += 1

    if i == 0:
        detectando.clear()

    i = 0
#se contorno for zero limpa a lista
    if len(contours) == 0:
        detectando.clear()

    else:

        for detect in detectando:
            for (c,l) in enumerate(detect):

                 #idetificando a posição antiga e atual
                if detect[c-1][1] < posL and l[1] > posL :
                    detect.clear()
                    cima+=1
                    total+=1
                    cv2.line(frame,xy1,xy2,(0,255,0),5)
                    continue
        #de baixo para cima
                if detect[c-1][1] > posL and l[1] < posL:
                    detect.clear()
                    baixo+=1
                    total+=1
                    cv2.line(frame,xy1,xy2,(0,0,255),5)
                    continue

                if c > 0:
                    cv2.line(frame,detect[c-1],l,(0,0,255),1)

    cv2.putText(frame, "TOTAL de peixes : "+str(total), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255),2)


    cv2.imshow("frame", frame)
 #para quando acaba o vídeo.
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()