import io,itertools,struct,unittest
from read_gfs_index import read_index
from input_edges import render_buttons,mirror_direction

def fixture():
    def string(s):b=s.encode();return struct.pack('>Q',len(b))+b
    index=string('Reverge Package File')+string('1.1')+struct.pack('>Q',1)+string('synthetic.txt')+struct.pack('>QI',3,4)
    start=4+len(index);offset=start+(-start)%4
    return struct.pack('>I',start)+index+bytes(offset-start)+b'abc'

class Examples(unittest.TestCase):
    def test_index_size_alignment_and_path(self):
        data=fixture();r=read_index(io.BytesIO(data),len(data));e=r['entries'][0]
        self.assertEqual(e['path'],'synthetic.txt');self.assertEqual(e['offset']%4,0)
        self.assertEqual(data[e['offset']:e['offset']+e['size']],b'abc')
    def test_all_truncations_rejected(self):
        data=fixture()
        for n in range(len(data)):
            with self.assertRaises(ValueError):read_index(io.BytesIO(data[:n]),n)
    def test_version_mismatch_rejected(self):
        data=fixture().replace(b'1.1',b'2.0')
        with self.assertRaises(ValueError):read_index(io.BytesIO(data),len(data))
    def test_press_hold_release_up(self):
        up=[False]*4;down=[True,False,False,False]
        self.assertEqual(render_buttons(up,down),[0,4,4,4]);self.assertEqual(render_buttons(down,down),[3,4,4,4])
        self.assertEqual(render_buttons(down,up),[1,4,4,4]);self.assertEqual(render_buttons(up,up),[4]*4)
    def test_all_synthetic_physical_combinations(self):
        combos=list(itertools.product((False,True),repeat=4))
        for a in combos:
            for b in combos:self.assertTrue(set(render_buttons(a,b)).issubset({0,1,3,4}))
    def test_direction_reflection_is_involution(self):
        for d in range(9):self.assertEqual(mirror_direction(mirror_direction(d)),d)
    def test_invalid_input_rejected(self):
        with self.assertRaises(ValueError):render_buttons([0]*4,[False]*4)
        with self.assertRaises(ValueError):mirror_direction(9)

if __name__=='__main__':unittest.main()
