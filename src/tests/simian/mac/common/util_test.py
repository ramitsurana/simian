#!/usr/bin/env python
#
# Copyright 2011 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#

"""util module tests."""




import mox
import stubout

from google.apputils import app
from google.apputils import basetest
from simian.mac.common import util


class DatetimeTest(mox.MoxTestBase):

  def setUp(self):
    mox.MoxTestBase.setUp(self)
    self.stubs = stubout.StubOutForTesting()
    self.dt = util.Datetime

  def tearDown(self):
    self.mox.UnsetStubs()
    self.stubs.UnsetAll()

  def testUtcFromTimestampInt(self):
    """Tests utcfromtimestamp()."""
    expected_datetime = util.datetime.datetime(2011, 8, 8, 15, 42, 59)
    epoch = 1312818179
    self.assertEqual(expected_datetime, self.dt.utcfromtimestamp(epoch))

  def testUtcFromTimestampFloat(self):
    """Tests utcfromtimestamp()."""
    expected_datetime = util.datetime.datetime(2011, 8, 8, 15, 42, 59)
    epoch = 1312818179.1415989
    self.assertEqual(expected_datetime, self.dt.utcfromtimestamp(epoch))

  def testUtcFromTimestampString(self):
    """Tests utcfromtimestamp()."""
    expected_datetime = util.datetime.datetime(2011, 8, 8, 15, 42, 59)
    epoch = '1312818179.1415989'
    self.assertEqual(expected_datetime, self.dt.utcfromtimestamp(epoch))

  def testUtcFromTimestampNone(self):
    """Tests utcfromtimestamp() with None as epoch time."""
    self.assertRaises(ValueError, self.dt.utcfromtimestamp, None)

  def testUtcFromTimestampInvalid(self):
    """Tests utcfromtimestamp() with None as epoch time."""
    self.assertRaises(ValueError, self.dt.utcfromtimestamp, 'zz')

  def testUtcFromTimestampUnderOneHourInFuture(self):
    """Tests utcfromtimestamp() with epoch under one hour in the future."""
    epoch = util.time.time() + 600.0  # add ten minutes
    self.assertRaises(
        util.EpochFutureValueError, self.dt.utcfromtimestamp, epoch)

  def testUtcFromTimestampOverOneHourInFuture(self):
    """Tests utcfromtimestamp() with epoch over one hour in the future."""
    epoch = util.time.time() + 4000.0  # add a bit more than 1 hour
    self.assertRaises(
        util.EpochExtremeFutureValueError,
        self.dt.utcfromtimestamp, epoch)


class UtilModuleTest(mox.MoxTestBase):

  def setUp(self):
    mox.MoxTestBase.setUp(self)
    self.stubs = stubout.StubOutForTesting()

  def tearDown(self):
    self.mox.UnsetStubs()
    self.stubs.UnsetAll()

  def testSerializeJson(self):
    """Test Serialize()."""
    self.mox.StubOutWithMock(util.json, 'dumps')

    util.json.dumps('object1').AndReturn('serial1')
    util.json.dumps('object2').AndRaise(TypeError)

    self.mox.ReplayAll()
    self.assertEqual('serial1', util.Serialize('object1'))
    self.assertRaises(util.SerializeError, util.Serialize, 'object2')
    self.mox.VerifyAll()

  def testDeserializeJson(self):
    """Test Deserialize()."""
    self.mox.StubOutWithMock(util.json, 'loads')

    util.json.loads('serial1', parse_float=float).AndReturn('object1')
    util.json.loads('serial2', parse_float=float).AndRaise(ValueError)

    self.mox.ReplayAll()
    self.assertEqual('object1', util.Deserialize('serial1'))
    self.assertRaises(util.DeserializeError, util.Deserialize, 'serial2')
    self.mox.VerifyAll()

  def testDeserializeWhenNone(self):
    """Test Deserialize()."""
    self.mox.ReplayAll()
    self.assertRaises(util.DeserializeError, util.Deserialize, None)
    self.mox.VerifyAll()

  def testUrlUnquote(self):
    """Test UrlUnquote()."""
    self.assertEqual(util.UrlUnquote('foo'), 'foo')
    self.assertEqual(util.UrlUnquote('foo%2F'), 'foo/')
    self.assertEqual(util.UrlUnquote('foo<ohcrap>'), 'foo<ohcrap>')


def main(unused_argv):
  basetest.main()


if __name__ == '__main__':
  app.run()
