"""作者：Wangyuan；日期：2026-11-08。职责：通过合成输入复验已确认缺陷。"""
import unittest
from core import run
class ReleaseTests(unittest.TestCase):
 def test_overflowing_finite_interval_rejected(self) -> None:
  with self.assertRaises(ValueError):run({'snapshots':[{'time':-1e308,'counts':{'x':0}},{'time':1e308,'counts':{'x':1}}]})
 def test_unrepresentable_rate_rejected(self) -> None:
  with self.assertRaises(ValueError):run({'snapshots':[{'time':0,'counts':{'x':0}},{'time':1,'counts':{'x':10**400}}]})
