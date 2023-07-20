# DesicionTreeRejectRegulationMining
## 金融风控领域 决策树拒绝规则挖掘


### 多头决策树拒绝策略
#### 1.	停止条件
	
&emsp;&emsp;最差1箱客群（要占比3%以内，同时这一箱的bad_rate值要尽量高，LIFT>=2)  (原理是这一箱整体会被拒绝，所以希望拒绝的这一箱的人尽可能少,同时坏人占比尽可能的高)  多头的意思是指：同时/一段时间内在多个非银/银行机构的借款，即多头借贷。

#### 2.	筛选变量
&emsp;&emsp;因为是准入阶段的拒绝策略，所以非准入阶段的变量和与业务无关的全部不能使用。

&emsp;&emsp;准入阶段的变量举例：</br></br>
&emsp;&emsp;&emsp;&emsp;als_d15_id_nbank_orgnum： 按身份证（id）查询 15天内_在非银机构（org）借贷的次数（num）</br>
&emsp;&emsp;&emsp;&emsp;als_m3_cell_nbank_inteday :  按手机号（cell）查询 3个月内_在非银机构xxx的间隔 （不是很懂）</br></br>

			
&emsp;&emsp;非准入阶段的变量包括：max_ovd（历史最大逾期天数）、mob（账龄）、repay_dt（还款日）、利率、分期期数等等。

&emsp;&emsp;与业务无关的变量包括：crdt_appl_dt（申请年月日），In_distr_dt（放款日）, crtf_num ( 身份号码 )、serial_num( 流水号 )，crdt_seq_id、dubil_num( 订单号 )


#### 3.	验证方式：
&emsp;&emsp;从样本中划出train和test 使用OOT（out of time）验证，需要采用申请日期appl_dt排序，比例7:3即可
观察PSI值

&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<img width="417" alt="image" src="https://github.com/ErwanPishi/DesicionTreeRejectRegulationMining-/assets/136585409/89589a2e-042f-45cb-80d2-b67472d7bc36">

#### 4. 变量准入
&emsp;&emsp;采用IV值靠前的变量10个以内进入策略（不一定全用，决策树的结构最多三层即可）分箱后必须要满足bad_rate从业务逻辑上单调(但是如果变量的PSI够低，也可以在业务逻辑上反着），构造出三层或四层的决策树模型，人工暴力嗯点，缺失值最好单独分成一箱 FICO@MODEL_BUILDER你tm能不能敢再给爷卡一点

#### 5. 具体结构：
&emsp;&emsp;num_split  from 4 to 6，不要二叉，二叉的话限制太大，需要分很多层</br></br>
&emsp;&emsp;max_depth = 4</br></br>
&emsp;&emsp;所以最后得到的leaf_nodes最多有6^3 = 216个，最后要把这216个nodes分别打上treatment ，bad_rate相近的是一个treatment</br></br>
&emsp;&emsp;最后把leaf_nodes合并成5箱就合适了，箱与箱之间badrate差距至少要在1%以上</br>

#### 6. UAT (User Acceptance Test) ?????


