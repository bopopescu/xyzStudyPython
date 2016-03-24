#_*_ coding:utf-8 _*_
import Tkinter
import tkFileDialog
import ScrolledText
from xyz_lib.utils import fn_timer


#在类的外部定义一个新建记事本的函数
def newNote():
    notepad()
class notepad:
    def __init__(self):
        #生成主容器
        self.root=Tkinter.Tk()
        self.root.geometry('700x600')
        #初始化菜单栏
        self.menubar=Tkinter.Menu(self.root)
        self.submenu1=Tkinter.Menu(self.menubar,tearoff=0)
        
        self.submenu1.add_command(label="新建",command=newNote)
        self.submenu1.add_command(label="打开",command=self.FileOpen)
        self.submenu1.add_command(label="保存",command=self.FileSave)
        self.submenu1.add_separator()
        self.submenu1.add_command(label="退出",command=self.exit)
        
        self.menubar.add_cascade(label="文件",menu=self.submenu1)
        
        self.root.config(menu=self.menubar)
        
        
        self.frame=Tkinter.Frame(self.root,bg='pink',width=700,height=600)
        self.frame.pack()
        #ScrollText:带滚动条的文本框,ScrollText里有insert(index,char)方法(插入文字)
        #            和get(index1,index2)方法
        self.st=ScrolledText.ScrolledText(self.frame,background='white',width=700,height=600)
        self.st.pack(side='left')
        
        self.root.mainloop()
    
    #打开文件
    @fn_timer
    def FileOpen(self):
        end='end'
        #openDlg是返回的文件路径
        openDlg=tkFileDialog.askopenfilename(title='open',initialdir='h:/')
        if openDlg:
            p=open(openDlg,'r')
            for line in p:
                self.st.insert(end, line)
            p.close()
    #保存文件    
    def FileSave(self):
        saveDlg=tkFileDialog.asksaveasfilename(initialdir='h:/')
        if saveDlg:
            p=open(saveDlg,'w')
            p.write(self.st.get(1.0,"end"))
            p.close()
    #退出记事本
    def exit(self):
        self.root.destroy()
        
        

if __name__=='__main__':

    note = notepad()
