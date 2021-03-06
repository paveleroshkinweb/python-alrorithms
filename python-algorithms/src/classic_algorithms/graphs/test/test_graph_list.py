import unittest
from graph_list import Graph
from oriented_graph import Graph as OrientedGraph
import utils


class TestGraph(unittest.TestCase):

    def test_add_vertex(self):
        graph = Graph()
        graph.add_vertex(5)
        graph.add_vertex(1)
        graph.add_vertex(2)
        self.assertSequenceEqual([], graph.adjacency_list[5])
        self.assertSequenceEqual([], graph.adjacency_list[1])
        self.assertSequenceEqual([], graph.adjacency_list[2])
        with self.assertRaises(Exception):
            graph.add_vertex(5)

    def test_add_edge(self):
        graph = Graph()
        graph.add_vertex(5)
        graph.add_vertex(1)
        graph.add_vertex(2)
        graph.add_edge(5, 1)
        graph.add_edge(5, 2)
        graph.add_edge(3, 4)
        self.assertSequenceEqual([1, 2], graph.adjacency_list[5])
        self.assertSequenceEqual([5], graph.adjacency_list[1])
        self.assertSequenceEqual([5], graph.adjacency_list[2])
        self.assertSequenceEqual([3], graph.adjacency_list[4])
        self.assertSequenceEqual([4], graph.adjacency_list[3])

    def test_remove_edge(self):
        graph = Graph()
        graph.add_edge(1, 2)
        graph.add_edge(1, 3)
        graph.add_edge(1, 4)
        graph.add_edge(2, 4)
        graph.add_edge(3, 4)
        graph.remove_edge(1, 2)
        self.assertSequenceEqual([3, 4], graph.adjacency_list[1])
        self.assertSequenceEqual([4], graph.adjacency_list[2])
        graph.remove_edge(2, 4)
        self.assertSequenceEqual([], graph.adjacency_list[2])
        self.assertSequenceEqual([1, 3], graph.adjacency_list[4])
        with self.assertRaises(Exception):
            graph.remove_edge(5, 10)
            graph.remove_edge(1, 2)

    def test_get_all_vertices(self):
        graph = Graph()
        self.assertSequenceEqual([], graph.get_all_vertices())
        graph.add_vertex(1)
        graph.add_vertex(2)
        graph.add_vertex(3)
        graph.add_edge(4, 5)
        self.assertSetEqual(set([1, 2, 3, 4, 5]), set(graph.get_all_vertices()))

    def test_get_vertex_environment(self):
        graph = Graph()
        graph.add_edge(1, 2)
        graph.add_edge(1, 3)
        graph.add_edge(2, 4)
        self.assertSequenceEqual([2, 3], graph.get_vertex_environment(1))
        self.assertSequenceEqual([1, 4], graph.get_vertex_environment(2))
        self.assertEqual([], graph.get_vertex_environment(100))

    def test_is_adjacent_vertices(self):
        graph = Graph()
        graph.add_edge(1, 2)
        graph.add_edge(3, 4)
        self.assertTrue(graph.is_adjacent_vertices(1, 2))
        self.assertTrue(graph.is_adjacent_vertices(3, 4))
        self.assertFalse(graph.is_adjacent_vertices(1, 4))
        self.assertFalse(graph.is_adjacent_vertices(5, 10))

    def test_is_connected(self):
        graph = Graph()
        graph.add_edge(1, 2)
        graph.add_edge(2, 3)
        graph.add_edge(2, 4)
        graph.add_edge(3, 4)
        self.assertTrue(utils.is_graph_connected(graph))
        graph.add_edge(5, 6)
        self.assertFalse(utils.is_graph_connected(graph))

    def test_is_bipartite(self):
        graph = Graph()
        self.assertTrue(utils.is_bipartite(graph))
        graph.add_vertices([1, 2, 3])
        self.assertTrue(utils.is_bipartite(graph))
        graph.add_edge(1, 2)
        graph.add_edge(3, 4)
        graph.add_edge(1, 4)
        graph.add_edge(2, 3)
        graph.add_edge(4, 5)
        graph.add_edge(5, 6)
        self.assertTrue(utils.is_bipartite(graph)[0])
        graph.add_edge(1, 5)
        self.assertFalse(utils.is_bipartite(graph)[0])
        graph = Graph()
        graph.add_edges([(1, 5), (2, 5), (2, 6), (6, 7), (7, 3), (7, 4)])
        self.assertTrue(utils.is_bipartite(graph)[0])
        graph = Graph()
        graph.add_edges([(1, 4), (2, 4), (1, 2), (2, 5), (5, 3)])
        self.assertFalse(utils.is_bipartite(graph)[0])

    def test_is_acyclic_graph(self):
        graph = Graph()
        self.assertTrue(utils.is_acyclic_graph(graph))
        graph.add_edge(1, 2)
        graph.add_edge(2, 3)
        graph.add_edge(1, 3)
        self.assertFalse(utils.is_acyclic_graph(graph))
        graph.remove_edge(1, 3)
        self.assertTrue(utils.is_acyclic_graph(graph))
        graph.add_edge(2, 4)
        graph.add_edge(3, 4)
        self.assertFalse(utils.is_acyclic_graph(graph))
        graph.remove_edge(3, 4)
        self.assertTrue(utils.is_acyclic_graph(graph))
        graph.add_edge(3, 5)
        graph.add_edge(3, 7)
        graph.add_edge(5, 7)
        self.assertFalse(utils.is_acyclic_graph(graph))

    def test_dfs(self):
        graph = OrientedGraph()
        self.assertSequenceEqual([], graph.depth_first_search())
        graph.add_edge(1, 2)
        graph.add_edge(1, 3)
        graph.add_edge(4, 2)
        graph.add_edge(4, 3)
        graph.add_edge(3, 2)
        self.assertSequenceEqual([1, 2, 3, 4], graph.depth_first_search())
        graph = OrientedGraph()
        graph.add_edge(1, 2)
        graph.add_edge(2, 3)
        graph.add_edge(1, 5)
        graph.add_edge(5, 6)
        self.assertSequenceEqual([1, 2, 3, 5, 6], graph.depth_first_search())

    def test_topological_sort(self):
        graph = OrientedGraph()
        graph.add_edges([(1, 2), (1, 3), (3, 2), (3, 10), (3, 11), (10, 11)])
        self.assertSequenceEqual([1, 3, 2, 10, 11], graph.topological_sort())
        graph.add_edges([(2, 4), (4, 5), (4, 6), (6, 7), (5, 7)])
        self.assertSequenceEqual([1, 3, 2, 4, 5, 6, 7, 10, 11], graph.topological_sort())
        graph.add_edges([(5, 9), (7, 9), (7, 8), (9, 8)])
        self.assertSequenceEqual([1, 3, 2, 4, 5, 6, 7, 9, 8, 10, 11], graph.topological_sort())
        graph.add_edges([(8, 12), (12, 7)])
        self.assertIsNone(graph.topological_sort())

    def test_prim(self):
        graph = Graph()
        total_cost, _ = utils.prim(graph)
        self.assertEqual(0, total_cost)
        graph.add_edge('A', 'D', 5)
        graph.add_edge('A', 'B', 7)
        graph.add_edge('D', 'B', 9)
        graph.add_edge('D', 'E', 15)
        graph.add_edge('B', 'E', 7)
        graph.add_edge('B', 'C', 8)
        graph.add_edge('C', 'E', 5)
        graph.add_edge('D', 'F', 6)
        graph.add_edge('E', 'G', 9)
        graph.add_edge('F', 'G', 11)
        graph.add_edge('F', 'E', 8)
        total_cost, result_graph = utils.prim(graph)
        self.assertEqual(39, total_cost)
        self.assertEqual(7, len(result_graph.get_all_vertices()))
        self.assertTrue(utils.is_graph_connected(result_graph))
        self.assertTrue(utils.is_acyclic_graph(result_graph))

    def test_kruskal(self):
        graph = Graph()
        total_cost, _ = utils.kruskal(graph)
        self.assertEqual(0, total_cost)
        graph.add_edge('A', 'D', 5)
        graph.add_edge('A', 'B', 7)
        graph.add_edge('D', 'B', 9)
        graph.add_edge('D', 'E', 15)
        graph.add_edge('B', 'E', 7)
        graph.add_edge('B', 'C', 8)
        graph.add_edge('C', 'E', 5)
        graph.add_edge('D', 'F', 6)
        graph.add_edge('E', 'G', 9)
        graph.add_edge('F', 'G', 11)
        graph.add_edge('F', 'E', 8)
        total_cost, result_graph = utils.kruskal(graph)
        self.assertEqual(39, total_cost)
        self.assertEqual(7, len(result_graph.get_all_vertices()))
        self.assertTrue(utils.is_graph_connected(result_graph))
        self.assertTrue(utils.is_acyclic_graph(result_graph))

    def test_euler_cycle(self):
        graph = Graph()
        self.assertIsNone(utils.find_euler_cycle(graph))
        graph.add_edge(1, 2)
        graph.add_edge(1, 3)
        self.assertIsNone(utils.find_euler_cycle(graph))
        graph.add_edge(2, 3)
        self.assertSequenceEqual([1, 2, 3, 1], utils.find_euler_cycle(graph))
        graph.add_edge(2, 4)
        graph.add_edge(2, 6)
        graph.add_edge(3, 6)
        graph.add_edge(3, 5)
        graph.add_edge(5, 6)
        graph.add_edge(5, 4)
        graph.add_edge(4, 6)
        graph.add_edge(4, 7)
        graph.add_edge(5, 7)
        self.assertSequenceEqual([1, 2, 4, 6, 5, 7, 4, 5, 3, 6, 2, 3, 1], utils.find_euler_cycle(graph, 1))

    def test_dsatur(self):
        graph = Graph()
        graph.add_edges([(1, 2), (1, 7), (2, 3), (7, 6), (6, 3), (3, 4), (6, 4), (6, 5), (5, 4)])
        vertices_colors, used_colors = utils.dsatur(graph)
        self.assertDictEqual({6: 0, 3: 1, 4: 2, 5: 1, 2: 0, 1: 1, 7: 2}, vertices_colors)
        self.assertEqual(used_colors, 3)

    def test_gis(self):
        graph = Graph()
        graph.add_edges([(1, 2), (1, 7), (2, 3), (7, 6), (6, 3), (3, 4), (6, 4), (6, 5), (5, 4)])
        vertices_colors, used_colors = utils.gis(graph)
        self.assertDictEqual({1: 0, 5: 0, 3: 0, 2: 1, 4: 1, 7: 1, 6: 2}, vertices_colors)
        self.assertEqual(used_colors, 3)

    def test_djkstra(self):
        graph = OrientedGraph()
        graph.add_edge(1, 2, 2)
        graph.add_edge(1, 3, 3)
        graph.add_edge(2, 4, 3)
        graph.add_edge(2, 6, 2)
        graph.add_edge(3, 4, 1)
        graph.add_edge(3, 5, 1)
        graph.add_edge(4, 5, 2)
        graph.add_edge(4, 6, 4)
        graph.add_edge(5, 6, 1)
        self.assertEqual((4, [1, 2, 6]), utils.djkstra(graph, 1, 6))
        self.assertIsNone(utils.djkstra(graph, 4, 3))
        self.assertEqual((2, [3, 5, 6]), utils.djkstra(graph, 3, 6))

    def test_tsp(self):
        graph = Graph()
        graph.add_edges([(1, 2, 5), (1, 3, 2), (1, 4, 1), (1, 5, 7), (2, 3, 4), (2, 4, 3), (2, 5, 2), (3, 4, 3), (3, 5, 6), (4, 5, 4)])
        self.assertEqual([1, 4, 5, 2, 3], utils.tsp(graph))


if __name__ == 'main':
    unittest.main()
