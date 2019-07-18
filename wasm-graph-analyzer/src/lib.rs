mod utils;

use wasm_bindgen::prelude::*;

extern crate web_sys;
extern crate js_sys;

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
    nb_nodes: u32,
    nb_neighbors_by_node: u32,
    neighbors: Vec<u32>
}

impl Graph {
    fn get_random_neighbor(&self, node_id: u32) -> u32 {
        self.neighbors[(node_id*self.nb_neighbors_by_node + (js_sys::Math::random()*self.nb_neighbors_by_node as f64) as u32) as usize] as u32
    }
}

#[wasm_bindgen]
impl Graph {
    pub fn new(nb_nodes: u32, nb_neighbors_by_node: u32, neighbors: Vec<u32>) -> Graph {
        Graph {
            nb_nodes,
            nb_neighbors_by_node,
            neighbors,
        }
    }
    pub fn random_walk(&self, nb_iterations: u32) -> u32 {
        let mut current_node = (js_sys::Math::random()*self.nb_nodes as f64) as u32;

        for iteration in 0..nb_iterations {
            current_node = self.get_random_neighbor(current_node);
        }
        current_node
    }
}
