import {library} from '@fortawesome/fontawesome-svg-core';
import {
    faCaretDown,
    faCaretRight,
    faPen,
    faPlus,
    fas,
    faTrashAlt,
    faTimesCircle,
    faTimes,
} from '@fortawesome/free-solid-svg-icons';
import FontAwesomeIcon from '@/lib/FontAwesomeIcon.vue';

library.add(
    fas,
    faCaretDown,
    faCaretRight,
    faPlus,
    faTrashAlt,
    faPen,
    faTimesCircle,
    faTimes,
);

export {FontAwesomeIcon};