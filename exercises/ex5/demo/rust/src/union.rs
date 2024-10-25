use scanf::scanf;

#[derive(Debug)]
enum Options {
    A(i32),
    B(f32),
}

fn main() {
    let mut i = 0;
    print!("input value for Option::A: ");
    scanf!("{}", i).unwrap();

    let o = Options::A(i);

    // println!("o.A {}", o.A);
    // println!("o.B {}", o.B);

    if let Options::A(inner) = o {
        println!("Option::A: {:?}", o);
        println!("Option::B by explict cast: {:?}", Options::B(inner as f32));
    }
}
