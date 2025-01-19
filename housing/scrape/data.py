# In-memory database wrapper
import os, dataclasses as dc, datetime as dt
import polars as pl

from .model import House, Address

class Database:

	data_path	 = './data/'
	housing_file = data_path + 'houses.parquet'
	areas_file   = data_path + 'areas.parquet'

	def __init__(self):

		self._houses: pl.DataFrame = (
			pl.read_parquet(self.housing_file) 
			if os.path.isfile(self.housing_file) 
			else pl.DataFrame()
		)
		self._areas: pl.DataFrame = (
			pl.read_parquet(self.areas_file) 
			if os.path.isfile(self.areas_file) 
			else pl.DataFrame()
		)

	def __enter__(self): return self
	def __exit__(self, type, value, traceback):
		os.makedirs(self.data_path, exist_ok=True)
		self._houses.write_parquet(self.housing_file)
		self._areas.write_parquet(self.areas_file)
		print(f'saved database to {self.housing_file}')

	def addresses(self) -> list[Address]: 
		if 'address' not in self._houses.columns: return []
		return map(
			lambda row: Address(**row['address']), 
			self._houses.iter_rows(named = True)
		)

	def houses(self) -> list[House]: 
		if 'address' not in self.houses.columns: return [] 
		return map(
			lambda row: House(**(row | {'address': Address(row['address'])})),
			self._houses.iter_rows(named=True)
		)

	def add(self, *houses): 

		addresses = set(self.addresses())
		not_in_db = set(filter(lambda house: house.address not in addresses, houses))

		if len(not_in_db) > 0:  
			self._houses = self._houses.vstack(
				pl.DataFrame([dc.asdict(house) for house in not_in_db])
			)
			not_in_db_str = '\n'.join(map(str, not_in_db))
			print(f'added {len(not_in_db)} new houses: \n{not_in_db_str}')
		else: 
			print(f'no new houses, {len(self._houses)} in db')

		# todo: if it is, check for equality, 
		# if different, warn user and update
		return not_in_db 

