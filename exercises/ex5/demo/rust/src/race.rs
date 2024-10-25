
use std::thread;

// static mut counter: i32 = 0;

// fn increment_counter() {
//     for _  in 0..100000 {
//         counter += 1;
//         println!("counter: {}", counter);
//     }
// }

use std::sync::atomic::{AtomicI32, Ordering};

static counter: AtomicI32 = AtomicI32::new(0);

fn increment_counter() {
    for _  in 0..100000 {
        counter.fetch_add(1, Ordering::Relaxed);
        println!("counter: {:?}", counter);
    }
}

fn main() {
    let mut threads = Vec::new();

    for _ in 0..8 {
        threads.push(thread::spawn(increment_counter));
    }

    for t in threads{
        t.join().unwrap()
    }

    println!("counter = {:?}", counter);
}
