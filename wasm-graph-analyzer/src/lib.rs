mod utils;

use wasm_bindgen::prelude::*;
use rand::{Rng, SeedableRng};
use rand::rngs::SmallRng;


extern crate web_sys;
extern crate js_sys;
extern crate rand;

// A macro to provide `println!(..)`-style syntax for `console.log` logging.
macro_rules! log {
    ( $( $t:tt )* ) => {
        web_sys::console::log_1(&format!( $( $t )* ).into());
    }
}

// When the `wee_alloc` feature is enabled, use `wee_alloc` as the global
// allocator.
#[cfg(feature = "wee_alloc")]
#[global_allocator]
static ALLOC: wee_alloc::WeeAlloc = wee_alloc::WeeAlloc::INIT;

#[wasm_bindgen]
extern {
    fn alert(s: &str);
}

#[wasm_bindgen]
pub fn greet() {
    alert("Hello, wasm-graph-analyzer!");
}

#[wasm_bindgen]
pub struct Graph {
    nb_nodes: usize,
    nb_neighbors_by_node: usize,
    neighbors: Vec<usize>
}

impl Graph {
    fn get_random_neighbor(&self, node_id: usize) -> usize {
        20
    }
}

#[wasm_bindgen]
impl Graph {
    pub fn new(nb_nodes: usize, nb_neighbors_by_node: usize, neighbors: Vec<usize>) -> Graph {
        Graph {
            nb_nodes,
            nb_neighbors_by_node,
            neighbors,
        }
    }
    pub fn random_walk(&self, nb_iterations: usize) -> Vec<u32> {

        let mut rng = SmallRng::from_entropy();
        let mut nb_times_visited_nodes: Vec<u32> = Vec::new();
        for _node in 0..self.nb_nodes {
            nb_times_visited_nodes.push(0);
        }

        for init_node in 0..self.nb_nodes {

            for _tmp in 1..10 {
                let mut current_node = init_node;
                // let mut current_node: usize = (js_sys::Math::random()*self.nb_nodes as f64) as usize;


                nb_times_visited_nodes[current_node] += 1;
                // let mut rng = rand::thread_rng();
                for _iteration in 0..nb_iterations {
                    let selected_neighbor_index = rng.gen_range(0, self.nb_neighbors_by_node);
                    let node_row: usize = current_node*self.nb_neighbors_by_node;
                    current_node = self.neighbors[node_row + selected_neighbor_index];

                    nb_times_visited_nodes[current_node] += 1;
                }
            }
        }
        nb_times_visited_nodes
    }
}
