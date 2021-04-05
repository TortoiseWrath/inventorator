export class Decimal extends String {
    value(): Number {
        return parseFloat(this.toString());
    }
}
