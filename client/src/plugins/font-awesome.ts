import {library} from '@fortawesome/fontawesome-svg-core';
import {faCaretDown, faCaretRight, faPen, faPlus, fas, faTrashAlt} from '@fortawesome/free-solid-svg-icons';
import FontAwesomeIcon from '@/lib/FontAwesomeIcon.vue';

library.add(
    fas,
    faCaretDown,
    faCaretRight,
    faPlus,
    faTrashAlt,
    faPen,
);

export {FontAwesomeIcon};