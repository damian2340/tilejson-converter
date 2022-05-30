
import sys
import transformaciones as tr

type = sys.argv[1].lower()
rootTransform = [float(i) for i in sys.argv[2:5]]
if type == 'root':
    trRoot = tr.Rotator_b3dm(tr.translation_2_transform(rootTransform), 1.2)
    result = trRoot.get_transform()
    print(tr.transform_2_str(result))
elif type == 'child':
    transform = [float(i) for i in sys.argv[17:20]]
    trRoot = tr.Rotator_b3dm(tr.translation_2_transform(rootTransform), 1.2)
    result = trRoot.get_children_transform(tr.translation_2_transform(transform))
    print(tr.transform_2_str(result))
elif type == 'bounding':
    bounding = [float(i) for i in sys.argv[5:17]]
    trRoot = tr.Rotator_b3dm(tr.translation_2_transform(rootTransform), 1.2)
    result = trRoot.get_bounding(bounding)
    print(tr.bounding_2_str(result))
