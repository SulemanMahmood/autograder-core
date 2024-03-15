import Test.HUnit

test1 :: Test
test1 = TestCase (assertEqual "test" 0 1)

tests :: Test
tests = TestList [TestLabel "test1" test1]

main :: IO Counts
main = do
  runTestTT tests