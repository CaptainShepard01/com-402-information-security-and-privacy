use scanf::scanf;

fn main() {
    let mut index = 0;
    let array = [1, 2, 3, 4, 5, 6];

    print!("input array index: ");
    scanf!("{}", index).unwrap();

    println!("array[{}] = {}", index, array[index]);
}
