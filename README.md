# DesicionTreeRejectRegulationMining-
金融风控领域 决策树拒绝规则挖掘


多头决策树拒绝策略
1.	停止条件
最差1箱客群（要占比3%以内，同时这一箱的bad_rate值要尽量高，LIFT>=2）（原理是这一箱整体会被拒绝，所以希望拒绝的这一箱的人尽可能少,同时坏人占比尽可能的高） 多头的意思是指：同时/一段时间内在多个非银/银行机构的借款，即多头借贷。
2.	筛选变量
因为是准入阶段的拒绝策略，所以非准入阶段的变量和与业务无关的全部不能使用。

准入阶段的变量举例：
als_d15_id_nbank_orgnum： 按身份证（id）查询 __15天内___在非银机构（org）借贷的次数（num）
als_m3_cell_nbank_inteday :  按手机号（cell）查询__3个月内_在非银机构xxx的间隔 （不是很懂）
			
非准入阶段的变量包括：max_ovd（历史最大逾期天数）、mob（账龄）、repay_dt（还款日）、利率、分期期数等等。

与业务无关的变量包括：crdt_appl_dt（申请年月日），In_distr_dt（放款日）, crtf_num ( 身份号码 )、serial_num( 流水号 )，crdt_seq_id、dubil_num( 订单号 )


3.	验证方式：
从样本中划出train和test，观察PSI值

<img width="417" alt="image" src="https://github.com/ErwanPishi/DesicionTreeRejectRegulationMining-/assets/136585409/89589a2e-042f-45cb-80d2-b67472d7bc36">
