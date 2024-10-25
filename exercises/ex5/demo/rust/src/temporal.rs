fn main() {
    let boxed = Box::new(1);

    println!("boxed value: {}", boxed);

    drop(boxed);

    println!("dropping boxed ptr");

    // println!("access boxed after drop: {}", boxed);
}
