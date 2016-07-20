#!/usr/bin/env python
#
#  Resource Allocation module based on the user needs
#  Aravind Muthu - 2016
#
#  Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php
#  
#   Example: 
#  		N cpu for H hours P(?)
#		N(?) cpu for H houurs with maximum willing Price to pay
#		N cpu for H hours with max willing Price 
#	
#   TODO:
#	 	write unittest
#       Refactor code
#

from collections import defaultdict, OrderedDict
import locale
#init
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

#Server type with various sizes
server = [("large", 1), 
		  ("xlarge", 2), 
		  ("2xlarge", 4), 
		  ("4xlarge", 8), 
		  ("8xlarge", 16), 
		  ("10xlarge", 32)
		 ]
#Given server type with $ values


class ResourceAllocator(object):
	'''
		Resource alocator module class
		Which help to find the server type with price for an N given hours

		N cpu for H hours P(?)
		N(?) cpu for H houurs with maximum willing Price to pay
		N cpu for H hours with max willing Price 
	'''
	DEFAULT_HOURS = 1

	def __init__(self):

		self.cpuWithQuantity = []
		self.cpuTotalCost = 0
		self.returnVal = {}
		self.finalResult = []
		self.server = server
		self.maxCycleChecked = True

	def get_costs(self, instances, hours = DEFAULT_HOURS, cpus = 0, price = 0):
		'''Doc - get costs of server'''
		
		self.instances = instances
		self.hours = hours
		self.cpus = cpus
		self.price = float(price)
		self.cpuQty = 0

		print("Needed Serve CPU quantity",self.cpus, "\n")

		for region , v in self.instances.items():
			self.returnVal["region"] 		= region
			self.returnVal["servers"]		= self.__getServers(region,v)
			self.returnVal["total_cost"] 	= locale.currency(self.cpuTotalCost)
			self.finalResult.append(self.returnVal)
			self.returnVal = {}

		return self.finalResult

	def __getServers(self, region, cpuWithCost):
		'''
			Gets the server qunaity and generating cpu cost
			[(large, 2)]

		'''
		self.cpuQty = 0
		self.cpuWithQuantity = []
		while self.cpuQty < self.cpus:
			for serverType, serverCpuQty in reversed(self.server):
				self.__getCpuQuantity(serverType, serverCpuQty, region)

		# only trigger if price given and cpu not given
		if (self.price and not self.cpus):
			self.__getCpuForGivenPrice(region)

		return self.__getAggregateCpuQty()	

	def __getCpuForGivenPrice(self, region):
		'''
			Gets the cpu qunaity for an given hours and price
		'''
		self.maxCycleChecked = True

		while self.cpuTotalCost <= self.price and self.maxCycleChecked:
			count = 0
			updatedCost = self.cpuTotalCost
			for serverType, serverCpuQty in reversed(self.server):
				try:
					if (serverType in self.instances[region]):
						curcpuQty = self.cpuQty + serverCpuQty
						if (self.cpuTotalCost <= self.price):
							self.cpuQty = curcpuQty						
							serverCost = self.instances[region][serverType]
							self.cpuWithQuantity.append((str(serverType), (serverCpuQty, serverCost)))
							count += 1
				except Exception as error:
					print(error)
			
			self.__getAggregateCpuQty()
			if (count == 0 or self.cpuTotalCost == updatedCost):
				self.maxCycleChecked= False


	def __getCpuQuantity(self, serverType, serverCpuQty, region):
		'''
			Returns the server type, CPU quanity, with price 
			[('large', (1, 0.12)), ('large', (1, 0.12))])

		'''
		if (self.cpus):
			## server type 'large' 'xlarge' serverCpuQty 1, 2, 4, 8, 16, 32
			try:
				if (serverType in self.instances[region]):
					curcpuQty = self.cpuQty + serverCpuQty
					if (curcpuQty <= self.cpus):
						self.cpuQty = curcpuQty						
						serverCost = self.instances[region][serverType]
						self.cpuWithQuantity.append((str(serverType), (serverCpuQty, serverCost)))
					else:
						pass
			except Exception as error:
				print(error)	
	

	def __getAggregateCpuQty(self):
		'''
			Returns aggregated server with sum of qty
			input  :  [(large,1) (large,1)]
			output :  [(large, 2)]

			TODO: Write the below logic in comprehension way 
			      Use map, reduce, filter
		'''
		self.cpuTotalCost = 0
		qtyOfCpu = defaultdict(int)
		print("Overall Expected CPUS :\n", self.cpuWithQuantity)
		for k, i in self.cpuWithQuantity:
			if (self.price != 0):
				if (self.cpuTotalCost < self.price):
					self.cpuTotalCost += self.hours * i[1]
					qtyOfCpu[k] += i[0]
					if (self.cpuTotalCost > self.price):
						self.cpuTotalCost -=self.hours * i[1]
						qtyOfCpu[k] -= i[0]
						self.maxCycleChecked = False
			else:
				self.cpuTotalCost += i[1]
				qtyOfCpu[k] += i[0]

		if (self.hours and self.hours!= 1 and self.price == 0):
			self.cpuTotalCost = self.hours * self.cpuTotalCost 
		return qtyOfCpu.items()

if __name__ == '__main__':

	print("Self Test by providing below inputs")

	instances = {
		"us-east": {
			"large": 0.12,
			"xlarge": 0.23,
			"2xlarge": 0.45,
			"4xlarge": 0.774,
			"8xlarge": 1.4,
			"10xlarge": 2.82
		},
		"us-west": {
			"large": 0.14,
			"2xlarge": 0.413,
			"4xlarge": 0.89,
			"8xlarge": 1.3,
			"10xlarge": 2.97
		},
	}

	print("\n===============================\n")
	print("Given Input") 
	print("\n===============================\n")
	obj1 =  ResourceAllocator()
	print("2 cpu for 2 hours   		: Scenario 1")
	print("Output \n========================\n")
	print(obj1.get_costs(instances, 2, 2), "\n"*2)
	print("\n===============================\n")
	'''
	2 cpu for 3 hours
	#print(obj1.get_costs(instances, 2, 2))
	[{'total_cost': 0.56, 
	  'region': 'us-west', 
	  'servers': [('large', 2)]}, 
	 {'total_cost': 0.46, 
	  'region': 'us-east', 
	  'servers': [('xlarge', 2)]
	  }]
	'''


	

	print("Given Input") 
	print("\n===============================\n")
	obj2 =  ResourceAllocator()
	print("2 cpu for $0.36 for 3 hours  	: Scenario 2")
	print("Output \n========================\n")
	print(obj2.get_costs(instances, 2, 2, 0.46), "\n"*2)
	print("\n===============================\n")
	'''
	2 cpu for $0.36 for 3 hours
	#print(obj2.get_costs(instances, 2, 2, 0.46))
	[{'total_cost': 0.28, 
	  'region': 'us-west', 
	  'servers': [('large', 1)]
	  }, 
	 {'total_cost': 0.46, 
	  'region': 'us-east', 
	  'servers': [('xlarge', 2)]
	 }]

	'''
	# yet to write the logic and need to check if all other works fine
	obj3 =  ResourceAllocator()
	print("n cpu for $3 for 1 hours")
	print(obj3.get_costs(instances, 1, 0, 3), "\n"*2)
	