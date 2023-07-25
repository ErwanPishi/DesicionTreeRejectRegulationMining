# DesicionTreeRejectRegulationMining
## 金融风控领域 决策树反欺诈规则挖掘


### 多头决策树拒绝策略
#### 1.	停止条件
	
&emsp;&emsp;最差1箱客群（要占比3%以内，同时这一箱的bad_rate值要尽量高，LIFT>=1.5,但不可一昧追求bad_rate而让样本占比过小导致bad_rate方差大，每新增加一个bad就会导致bad_rate大幅度波动)  (原理是这一箱整体会被拒绝，所以希望拒绝的这一箱的人尽可能少,同时坏人占比尽可能的高)  多头的意思是指：同时/一段时间内在多个非银/银行机构的借款，即多头借贷。

#### 2.	筛选变量
&emsp;&emsp;因为是准入阶段的拒绝策略，所以非准入阶段的变量和与业务无关的全部不能使用。

&emsp;&emsp;准入阶段的变量举例：</br></br>
&emsp;&emsp;&emsp;&emsp;als_d15_id_nbank_orgnum： 按身份证（id）查询 15天内_在非银机构（org）借贷的次数（num）</br>
&emsp;&emsp;&emsp;&emsp;als_m3_cell_nbank_inteday :  按手机号（cell）查询 3个月内_在非银机构xxx的间隔 （不是很懂）</br></br>

			
&emsp;&emsp;非准入阶段的变量包括：max_ovd（历史最大逾期天数）、mob（账龄）、repay_dt（还款日）、利率、分期期数等等。

&emsp;&emsp;与业务无关的变量包括：crdt_appl_dt（申请年月日），In_distr_dt（放款日）, crtf_num ( 身份号码 )、serial_num( 流水号 )，crdt_seq_id、dubil_num( 订单号 )</br></br>
#### 一点体会：看到变量为空时不能马上归为缺失值，这时候需要查看数据词典，因为有可能变量为空并非代表没有查得，是代表该变量的记录为0。如7天内XX申请次数，空则代表7天内XX申请次数=0

#### 3.	验证方式：
&emsp;&emsp;从样本中划出train和test 使用OOT（out of time）验证，需要采用申请日期appl_dt排序，比例7:3即可
观察PSI值 注意PSI值是看样本的分布，先计算train、test样本落在不同标签内的分布比例 以test作为actual，train作为expected  计算PSI值
但是在反欺诈阶段，PSI是否稳定不是特别重要，可解释性也不是特别重要因为会开发很多个（几十上百个规则），你这一个规则可能会很快失效（暂时弃用，样本是每天都在更新，等哪天它又有法了再启用）但是没关系 我们还有一大堆其他的规则。更重要的是准确性（LIFT值），哪个最好用哪个

&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<img width="417" alt="image" src="https://github.com/ErwanPishi/DesicionTreeRejectRegulationMining-/assets/136585409/89589a2e-042f-45cb-80d2-b67472d7bc36">

#### 4. 变量准入
&emsp;&emsp;采用IV值靠前的变量10个以内进入策略（不一定全用，决策树的结构最多三层即可 分箱后必须要满足bad_rate从业务逻辑上单调(但是如果变量的PSI够低，也可以在业务逻辑上反着，变量PSI够低的话代表在这一段时间内很稳定，反了就反了嘛，反正结论是稳健的），构造出三层或四层的决策树模型，人工暴力嗯点，缺失值最好单独分成一箱 FICO@MODEL_BUILDER你tm能不能敢再给爷卡一点

#### 5. 具体结构：
&emsp;&emsp;num_split  from 4 to 6，不要二叉，二叉的话限制太大，需要分很多层</br></br>
&emsp;&emsp;max_depth = 4</br></br>
&emsp;&emsp;所以最后得到的leaf_nodes最多有6^3 = 216个，最后要把这216个nodes分别打上treatment ，bad_rate相近的是一个treatment</br></br>
&emsp;&emsp;最后把leaf_nodes合并成5箱就合适了，箱与箱之间badrate差距至少要在1%以上</br>

#### 6. 暴力破解：
&emsp;&emsp;如果是野蛮生长版决策树可以不用关注解释性的问题，只需要验证模型的稳定性，也即验证，在train上badrate最高的20箱，是否在test上面也满足相同的趋势，其他的就不管了，这种方式是用来扩充规则的，因为一个数据集需要开发足够多的规则，当可解释的规则都搞完了之后 这就是最后一招了</br></br>
&emsp;&emsp;
#### 6. UAT (User Acceptance Test) ?????


