import nuke
if nuke.NUKE_VERSION_MAJOR < 11:
    from PySide import QtCore, QtGui, QtGui as QtWidgets
else:
    from PySide2 import QtGui, QtCore, QtWidgets
    
class MyCustomPanel(QtWidgets.QWidget):
    InputCountNumber=0
    OutputCountNumber=0

#-----------------------------------------------------------------------------------------

    def __init__(self):
        super(MyCustomPanel, self).__init__()
        # 设置窗口为置顶
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
#-----------------------------------------------------------------------------------------

        #创建文本
        Signature = QtWidgets.QLabel("V1.0              Made by Merak_Lin")
        Signature_font = Signature.font()
        Signature_font.setPointSize(5)  # 设置字体大小
        Signature_font.setBold(True)     # 设置字体粗体
        Signature.setFont(Signature_font)

        
        #创建文本
        Header = QtWidgets.QLabel("  Set&Render   :)")
        Header_font = Header.font()
        Header_font.setPointSize(16)  # 设置字体大小
        Header_font.setBold(True)     # 设置字体粗体
        Header.setFont(Header_font)

        #创建空行
        Null_Line = QtWidgets.QLabel("")
        Null_Line_font = Null_Line.font()
        Null_Line_font.setPointSize(2)  # 设置字体大小
        Null_Line_font.setBold(True)
        Null_Line.setFont(Null_Line_font)

        #创建分割线
        Line = QtWidgets.QLabel("————Output&Input_Count————")
        Line_font = Line.font()
        Line_font.setPointSize(8)  # 设置字体大小
        Line_font.setBold(True)
        Line.setFont(Line_font)


        # 创建设置输出按钮
        SetOutputbutton = QtWidgets.QPushButton("Set OutPut")
        SetOutputbutton.clicked.connect(self.SetOutput_button_clicked)
         # 创建更新按钮
        Updatebutton = QtWidgets.QPushButton("Update Node_Count")
        Updatebutton.clicked.connect(self.Update)
        # 创建按钮
        SetInputbutton = QtWidgets.QPushButton("Set InPut")
        SetInputbutton.clicked.connect(self.SetInput_button_clicked)

        # 创建按钮
        ResetOutputbutton = QtWidgets.QPushButton("Reset")
        ResetOutputbutton.clicked.connect(self.Reset)

        # 创建按钮
        SetRenderbutton = QtWidgets.QPushButton("Render!!!")
        SetRenderbutton.clicked.connect(self.Render)
        SetRenderbutton.setFixedHeight(50)
        SetRenderbutton.setStyleSheet("color:LightBlue;")
        Render_font=SetRenderbutton.font()
        Render_font.setBold(True)
        Render_font.setPointSize(10)
        SetRenderbutton.setFont(Render_font)


        #OutPut计数框文本
        OutputCount = QtWidgets.QLabel("OutPut:")
        # 设置文本标签的字体和样式
        font = OutputCount.font()
        font.setPointSize(10)  # 设置字体大小
        OutputCount.setFont(font)
        # OutPut计数框
        self.Output_spin_box = QtWidgets.QSpinBox(self)
        self.Output_spin_box.setValue(self.OutputCountNumber)  # 设置默认值
        self.Output_spin_box.setMinimum(0)  # 设置最小值
        self.Output_spin_box.setFixedWidth(50)  # 设置宽度
        self.Output_spin_box.setFixedHeight(20)  # 设置高度
        self.Output_spin_box.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.Output_spin_box.setReadOnly(True)

        #InPut计数框文本
        InputCount = QtWidgets.QLabel("InPut:")
        # 设置文本标签的字体和样式
        font = InputCount.font()
        font.setPointSize(10)  # 设置字体大小
        InputCount.setFont(font)
        # InPut计数框
        self.Input_spin_box = QtWidgets.QSpinBox(self)
        self.Input_spin_box.setValue(self.InputCountNumber)  # 设置默认值
        self.Input_spin_box.setMinimum(0)  # 设置最小值
        self.Input_spin_box.setFixedWidth(50)  # 设置宽度
        self.Input_spin_box.setFixedHeight(20)  # 设置高度
        self.Input_spin_box.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.Input_spin_box.setReadOnly(True)


#------------------------------------------------------------------------------------------

        # 设置面板标题
        self.setWindowTitle("Set&Render :)")

        # 创建布局
        layout = QtWidgets.QVBoxLayout()
        self.setMinimumWidth(200)

        # 创建SetOutPutCount水平布局
        OutPut_layout = QtWidgets.QHBoxLayout()
        OutPut_layout.addWidget(OutputCount)
        OutPut_layout.addWidget(self.Output_spin_box)

        # 创建InPutCount水平布局
        InPut_layout = QtWidgets.QHBoxLayout()
        InPut_layout.addWidget(InputCount)
        InPut_layout.addWidget(self.Input_spin_box)

        # 添加按钮到竖直布局
        layout.addWidget(Header)
        layout.addWidget(SetOutputbutton)
        layout.addWidget(SetInputbutton)
        layout.addWidget(Updatebutton)
        layout.addWidget(SetRenderbutton)

        layout.addWidget(Null_Line)

        layout.addWidget(Line)
        
        layout.addLayout(OutPut_layout)
        layout.addLayout(InPut_layout)
        layout.addWidget(ResetOutputbutton)

        layout.addWidget(Null_Line)
        layout.addWidget(Signature)
        

        # 设置布局
        self.setLayout(layout)

#--------------------------------------------------------------------------------------------
    def SetOutput_button_clicked(self):
       tempnode=nuke.selectedNode()
       if tempnode.Class()=='Write':
            self.OutputCountNumber +=1
            self.Output_spin_box.setValue(self.OutputCountNumber)
            Output=nuke.nodes.Output()
            Output.setInput(0,tempnode)
            Output['tile_color'].setValue(4278190335)
            Output['note_font'].setValue("Verdana Bold")
       else:
            nuke.message('请选择Write"节点')


    def SetInput_button_clicked(self):
        
        tempnode=nuke.selectedNode()
        Input=nuke.nodes.Input()
        Input['tile_color'].setValue(4278190335)
        Input['note_font'].setValue("Verdana Bold")
        Input.setXYpos(tempnode.xpos()-100,tempnode.ypos()-100)
        tempnode.setInput(0,Input)

        self.InputCountNumber +=1
        self.Input_spin_box.setValue(self.InputCountNumber)

    def Render(self):
     #获取Output连接的Write节点
     write_nodes = [node.input(0) for node in self.Findnodes("Output")]
     #获取Input节点
     Input_nodes = [node for node in self.Findnodes("Input")]

     #检测Limit to range
     Write_Limit_Flag=0
     write_Limit_Name=''
     file_Flag=0
     file_Name=''
     for node in write_nodes:
        if node['use_limit'].value()==False:
           Write_Limit_Flag=0
           write_Limit_Name=[node.name()]
           break
        else:
           Write_Limit_Flag=1
      #检测file
     for node in write_nodes:
         if node['file'].value()=="":
            file_Flag=0
            file_Name=[node.name()]
            break
         else:
            file_Flag=1
     if ((self.InputCountNumber==self.OutputCountNumber)or ((self.InputCountNumber+1)==self.OutputCountNumber))and(self.OutputCountNumber!=0) and(Write_Limit_Flag!=0) and (file_Flag!=0):
        Input_list_count=0
        for node in write_nodes:
             first_frame = int(node['first'].value())
             last_frame = int(node['last'].value())
             nuke.execute(node, first_frame, last_frame)
             path=node["file"].value()
             if ((Input_list_count+1)==self.OutputCountNumber) and ((self.InputCountNumber+1)==self.OutputCountNumber):
                break
             Read=nuke.nodes.Read()
             Read["file"].setValue(path)
             Read["first"].setValue(first_frame)
             Read["last"].setValue(last_frame)
             Read.setXYpos(Input_nodes[Input_list_count].xpos(),Input_nodes[Input_list_count].ypos()+50)
             Read.setInput(0,Input_nodes[Input_list_count])
             Input_nodes[Input_list_count].dependent()[0].setInput(0,Read)
             Input_list_count +=1
             
     elif (Write_Limit_Flag==0 )and ((self.InputCountNumber==self.OutputCountNumber)or ((self.InputCountNumber+1)==self.OutputCountNumber))and(self.OutputCountNumber!=0)and (file_Flag!=0) :
        nuke.message(f'{write_Limit_Name}节点的limit to range没设置')
     elif (Write_Limit_Flag!=0) and ((self.InputCountNumber==self.OutputCountNumber)or ((self.InputCountNumber+1)==self.OutputCountNumber))and(self.OutputCountNumber!=0)and (file_Flag==0):
        nuke.message(f'{file_Name}节点的file输出路径没设置')
     elif (Write_Limit_Flag==0) and ((self.InputCountNumber==self.OutputCountNumber)or ((self.InputCountNumber+1)==self.OutputCountNumber))and(self.OutputCountNumber!=0)and (file_Flag==0):
        nuke.message(f'{file_Name}节点的file输出路径没设置以及{write_Limit_Name}节点的limit to range没设置')

     else :
        nuke.message('请点击Update或者检查是否为Input=Output或Input+1=Output')


    def Findnodes(self,node_class):
       # 指定要查找的节点类型
     target_node_type = node_class 
       # 获取所有的节点
     all_nodes = nuke.allNodes()
      # 筛选出选择节点类型的节点
     same_type_nodes = [node for node in all_nodes if node.Class() == target_node_type]
      # 排序
     same_type_nodes =sorted(same_type_nodes, key=self.sort_by_number)
     return same_type_nodes

    def sort_by_number(self,node):
    # 从节点名称中提取数字部分，例如 "Output3" 中的 3
     node_name = node.name()
     number = ''.join(filter(str.isdigit, node_name))
     return int(number)
    
    def Update(self):
       self.OutputCountNumber=len(self.Findnodes("Output"))
       self.InputCountNumber=len(self.Findnodes("Input"))
       self.Input_spin_box.setValue(self.InputCountNumber)
       self.Output_spin_box.setValue(self.OutputCountNumber)
            
    def Reset(self):
       inputnodes=self.Findnodes("Input")
       outputnodes=self.Findnodes("Output")
       for node in inputnodes:
          nuke.delete(node)
       for node in outputnodes:
          nuke.delete(node)
       self.OutputCountNumber=0
       self.InputCountNumber=0
       self.Input_spin_box.setValue(self.InputCountNumber)
       self.Output_spin_box.setValue(self.OutputCountNumber)

            

#--------------------------------------------------------------------------------------------
# 创建并显示面板
panel = MyCustomPanel()
def L_Write():
 panel.show()