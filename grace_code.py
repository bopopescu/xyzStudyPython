# ss = "Of zit kggd zitkt qkt ygxk ortfzoeqs wqlatzwqssl qfr zvg ortfzoeqs yggzwqssl. Fgv oy ngx vqfz zg hxz zitd of gft soft. piv dgfn lgsxzogfl qkt zitkt? Zolh:hstqlt eigfut zit ygkd gy zit fxdwtk ngx utz.Zit Hkgukqddtkl!"
ss = 'wqlatzwqssl'
max = ord('z')
min = ord('A')
for add in range(1, max-min + 1):
    new = []
    for index, c in enumerate(ss):
        if c == ' ' or c == '.' or c == '!' or c == ':':
            new.append(c)
            continue
        number = ord(c)
        number = (number + add - min) % (max - min + 1) + min
        new.append(chr(number))
    print "".join(new)


