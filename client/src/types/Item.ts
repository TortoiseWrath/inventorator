export interface Item {
    title?: string,
    id?: number,
    childCount?: number,
    parent?: number,
    value?: string,
    weight?: string,
    volume?: string,
    totalValue?: string,
    totalWeight?: string,
    totalVolume?: string,

    expanded?: boolean, // null at first, then true or false after first expanded
    showModal?: boolean, // null at first, then true or false after first shown
}

