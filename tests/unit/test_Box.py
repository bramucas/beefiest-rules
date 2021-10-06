import pytest
from beefiest_rules.explainer import Box

class TestBox:

    @pytest.fixture(scope="class")
    def custom_box(self):
        return Box(
           ["ax1", "ax2", "ax3"],
           [(2.0, 5.0), (0.5, 6.2), (-55.0, +100)]
       )

    def test_constructor_fail_features_None(self):
        with pytest.raises(ValueError) as _:
            Box(None, [(1,2), (1,2)])

    def test_constructor_fail_features_not_iterable(self):
        with pytest.raises(ValueError) as _:
            Box("feature1", [(1,2), (1,2)])

    def test_constructor_fail_boundaries_None(self):
        with pytest.raises(ValueError) as _:
            Box(["f1", "f2"], None)
        
    def test_constructor_fail_boundaries_not_iterable(self):
        with pytest.raises(ValueError) as _:
            Box(["f1", "f2"], 2)

    def test_constructor_fail_cardinality(self):
        with pytest.raises(ValueError) as _:
            Box(["f1", "f2", "f3"], [(1,2),(1,2)])

    def test_constructor_fail_features_empty(self):
        with pytest.raises(ValueError) as _:
            Box([], [(1,2),(1,2)])

    def test_constructor_fail_boundaries_empty(self):
        with pytest.raises(ValueError) as _:
            Box(["f1", "f2", "f3"], [])

    def test_contains_point(self, custom_box):
       assert (custom_box.contains_point((2.5, 1, 0)) == True)  # checks true
       assert (custom_box.contains_point((2.5, 1, 200)) == False)  # checks false
       # checks when equal to limits
       assert (custom_box.contains_point((2.0, 0.5, -55)) == True)  # left
       assert (custom_box.contains_point((5.0, 6.2, +100)) == True)  # right

    def test_contains_point_feature_names(self, custom_box):
        assert (custom_box.contains_point((3, 70), axis_names=["ax1", "ax3"]) == True)
        assert (custom_box.contains_point((3, 70), axis_names=["ax1", "ax2"]) == False)

    def test_contains_point_fail_cardinality(self, custom_box):
        with pytest.raises(ValueError) as _:
            custom_box.contains_point((1,2,3,4,5,6,7,8,9,10))
    
    def test_contains_point_fail_with_names(self, custom_box):
        with pytest.raises(ValueError) as _:
            custom_box.contains_point((1,2), axis_names=["ax1", "ax2", "ax3"])
