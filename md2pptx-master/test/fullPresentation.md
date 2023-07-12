template: Martin Template.pptx
pageTitleSize: 22
sectionTitleSize: 30
baseTextSize: 22
compactTables: 20
numbers: no
style.fgcolor.blue: 0000FF
style.fgcolor.red: FF0000
style.fgcolor.green: 00FF00
style.fgcolor.purple: FF00FF

# Full Presentation
Martin Packer, IBM


## Some Additional WLM-Related Information

### IEAOPT*xx* INITIMP=

* Sets Initiator Code WLM Importance
* Values are *0*, *1*, *2*, *3*, *E*
	* *0* means Dispatching Priority 254 (FE)
	* *1* ,*2*, or *3* — Defines that the initiator dispatching priority has to be lower than the dispatching priority for CPU critical work with the same or a higher importance level
		* If no service class with the CPU critical attribute and a corresponding or higher importance level is defined in the WLM policy, the dispatching priority is calculated in the same way as for parameter INITIMP=E
	* *E* - will be calculated in the same way as the enqueue promotion dispatching priority. The dispatching priority is calculated dynamically to ensure access to the processor. It should not impact high importance work; however, there is no guarantee that CPU critical work will always have a higher dispatching priority.
* SMF30ICU helps size this CPU requirement

### Percentile Goal Transaction Ending Buckets

|Bucket|Minimum % Of Goal|Maximum % of Goal|PI Value|
|-:|--:|--:|-:|
|1|0|**50**|0.5|
|2|50|60|0.6|
|3|60|70|0.7|
|4|70|80|0.8|
|5|80|90|0.9|
|6|90|**100**|1.0|
|7|100|110|1.1|
|8|110|120|1.2|
|9|120|130|1.3|
|10|130|140|1.4|
|11|140|150|1.5|
|12|150|200|2.0|
|13|200|**400**|4.0|
|14|**400**|**&infin;**|4.0|

### Service Class Periods

* "Transactions" accumulate <span class="blue">service</span>
    * Transactions can be eg DDF transactions, but also batch jobs
* Service is typically <span class="blue">CPU</span>
* Transactions start in Period 1
* When a transaction's service exceeds the <span class="blue">duration</span> for Period 1 it switches to Period 2
    * Duration is **not** Elapsed Time
    * Likewise from Period 2 to Period 3
* Each Service Class period can have its own goal
    * Usually later periods' goals have progressively lower importances
        * And progressively more relaxed response time targets<br/>
* RMF reports comprehensively on each Service Class period
    * In Workload Activity Report (SMF 72)
* **Note:** CICS and IMS transactions cannot have multi-period goals
